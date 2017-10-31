---
layout: post
title: 3 billion rows with R
date: 2017-10-31 14:25
comments: false
categories: Hive, R, Hadoop, groupby, mapreduce, parallel, bigdata
---


An [earlier post]({{ site.baseurl }}{% post_url
2017-10-30-hive-udaf-with-R.md %}) showed some of the basics of using Hive
with R, along with debugging.

This shows a more realistic use case. 

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
   columns show up in consecutive order. This is from the critical `CLUSTER
   BY station` statement.
3. Sends the now grouped output of the three columns as `stdin` to be
   processed by the command `Rscript piecewise_fd.R`.
4. Reads the results from `stdout`, overwriting the table
   `fundamental_diagram`.


Here's the core of the R script `piecewise_fd.R`. Explanations are comments
inline.

```
# Each working chunk to process has around 800K rows.
# So make this parameter larger than 800K.
# More generally this should be larger than the max chunk size that one
# would like to process in memory.
CHUNKSIZE = 1e6L

# This is the index for the column defining the groups
GROUP_INDEX = 1L

SEP = "\t"

# Columns for the variables of interest. 
col.names = c("station", "flow2", "occ2")
colClasses = c("integer", "integer", "numeric")

multiple_groups = function(queue, g = GROUP_INDEX) length(unique(queue[, g])) > 1


# Process an entire group.
# This function will change depending on the analysis to perform.
process_group = function(grp, outfile)
{
    #... specific to your analysis
       
    write.table(out, outfile, col.names = FALSE, row.names = FALSE
                , sep = SEP)
}


# Main stream processing
############################################################

stream_in = file("stdin")
open(stream_in)
stream_out = stdout()

# Initialize the queue
queue = read.table(stream_in, nrows = CHUNKSIZE, colClasses = colClasses
    , col.names = col.names, na.strings = "\\N")

while(TRUE) {
    while(multiple_groups(queue)) {
        # Pop the first group out of the queue
        nextgrp = queue[, GROUP_INDEX] == queue[1, GROUP_INDEX]
        working = queue[nextgrp, ]
        queue = queue[!nextgrp, ]

        try(process_group(working, stream_out))
    }

    # Fill up the queue
    nextqueue = read.table(stream_in, nrows = CHUNKSIZE
        , colClasses = colClasses, col.names = col.names, na.strings = "\\N")
    if(nrow(nextqueue) == 0) {
        try(process_group(queue, stream_out))
        break
    }
    queue = rbind(queue, nextqueue)
}
```


