---
layout: post
title: 3 billion rows with R
date: 2017-10-31 14:25
comments: false
categories: Hive, R, Hadoop, groupby, mapreduce, parallel, bigdata
---

### Summary

Combining [Apache Hive](https://hive.apache.org/) with the 
[R language](https://www.r-project.org/) reduced the run time of a practical
data analysis script from a couple days to 12 minutes.

### Introduction

Researchers have worked R and Hadoop for many years, i.e.  through
[Hadoop's streaming
interface](https://www.r-bloggers.com/integrating-r-with-apache-hadoop/) or
[RHIPE and deltarho](http://deltarho.org/). The approach with Hive
described here complements these efforts, while staying mostly higher
level.

[Yesterday's post]({{ site.baseurl }}{% post_url
2017-10-30-hive-udaf-with-R %}) showed some of the basics of using Hive
with R, along with debugging.  This post shows a more realistic use case
processing 3 billion rows of traffic sensor data.
Hive does the column selection and the group by; R performs the
calculation. Each group fits easily in worker memory, so each Hive worker
can apply an R script to the data, one group at a time. This technique
plays off the strengths of each system.  Hive handles storage, column
selection, basic filtering, sorting, fault tolerance, and parallelism. R
lets us express arbitrary analytic operations as R functions.

### SQL

This SQL query applies the transformation:

```{sql}
INSERT OVERWRITE TABLE fundamental_diagram
SELECT
TRANSFORM (station, flow2, occupancy2)
USING "Rscript piecewise_fd.R"
-- The names of all the variables that are produced
AS(station 
  , n_total 
  , n_middle 
  , n_high 
  )
FROM (
    SELECT station, flow2, occupancy2
    FROM pems 
    CLUSTER BY station
) AS tmp
;
```

This SQL does the following:
1. Selects three columns from the table `pems`. Selecting just the
   necessary columns for the transform reduces overhead.
2. Groups the selected columns so that the unique values of the `station`
   columns are streamed through the transform in consecutive order. The critical `CLUSTER
   BY station` statement guarantees this.
3. Sends the now grouped output of the three columns as `stdin` to be
   processed by the command `Rscript piecewise_fd.R`.
4. Reads the results from `stdout`, overwriting the table
   `fundamental_diagram`.

### R

This section explains what the core of the transforming R script
`piecewise_fd.R` does. This script should also work fine for stream
processing arbitrary amounts of plain text data. For example, if you have
100 GB of plain text files in a directory you could write:

```{R}
cat data/* | Rscript piecewise_fd.R > results.tsv
```

Assume that the data be begins initially grouped by some column, and
processing the largest group doesn't exceed available memory. Some
techniques can work around these assumptions, but I won't mention them
here.

```{R}
# Should be larger than the max chunk size that one
# would like to process in memory.
CHUNKSIZE = 1e6L

# I checked ahead of time that the largest working chunk is
# around 800K rows.
# So make it larger than 800K.

# These parameters are specific to my particular analysis
col.names = c("station", "flow2", "occ2")
colClasses = c("integer", "integer", "numeric")
GROUP_INDEX = 1L  # Corresponds to grouping by station
SEP = "\t"


multiple_groups = function(queue, g = GROUP_INDEX)
{
    length(unique(queue[, g])) > 1
}


# Process an entire group.
# This function will change depending on the analysis to perform.
# grp is one group of the data frame
process_group = function(grp, outfile)
{
    #... specific to your analysis
       
    write.table(out, outfile, col.names = FALSE, row.names = FALSE
                , sep = SEP)
}


# Main stream processing
############################################################

# NOT stdin()
stream_in = file("stdin")
open(stream_in)
stream_out = stdout()

# Initialize the queue, a group of rows waiting to be processed
queue = read.table(stream_in, nrows = CHUNKSIZE, colClasses = colClasses
    , col.names = col.names, na.strings = "\\N")

while(TRUE) {
    while(multiple_groups(queue)) {
        # Pop the first group out of the queue
        nextgrp = queue[, GROUP_INDEX] == queue[1, GROUP_INDEX]
        current = queue[nextgrp, ]
        queue = queue[!nextgrp, ]
        
        # Using try() allows each function to fail and keep going anyways.
        try(process_group(current, stream_out))
    }

    # Fill up the queue
    nextqueue = read.table(stream_in, nrows = CHUNKSIZE
        , colClasses = colClasses, col.names = col.names, na.strings = "\\N")
    if(nrow(nextqueue) == 0) {
        # This is the last group
        try(process_group(queue, stream_out))
        break
    }
    queue = rbind(queue, nextqueue)
}
```

I ran into a few gotcha's when writing this.  Hive represents missing
values with `\N` by default, so one needs to pass `na.strings = "\\N"` argument to
`read.table()`. Explicitly setting the `col.names` and `colClasses` fixed a
bug I ran into by ensuring consistency between how the data is stored in
Hive and in R.  Both of these things can be determined from Hive's metadata
store. Furthermore, very little of this R code is specific to my particular
analysis. In the future I would like to generalize and generate this code
rather than having to write it all explicitly.

Using `try(process_group(...)` from the R side allows the `process_group()`
function to fail silently. For this particular use case the analysis fails
for about half the groups because of issues in the data. This is completely
acceptable for my purposes.  However, for something that absolutely must
happen with every group you can remove the `try()` so that the failure will
propagate into the SQL query and the table will fail to be written.

### Conclusion

This post shows how to use R and Hive for `group by, apply` operations on
large data sets. The primary advantage is that each system does what it's
good at. Making R code parallel and scalable across vast amounts of text
data is certainly possible, but writing SQL is easier. Expressing a complex
analysis function as a native Hive UDF to process the groups with a `GROUP
BY` is also possible, but using a fast, robust implementation in an R
package is easier.

Another advantage is that no installation or configuration is required. If
you have data in Hive and R installed on the cluster then you can use this
technique today.
