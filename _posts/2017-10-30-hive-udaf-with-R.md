---
layout: post
title: hive udaf with R
date: 2017-10-30 14:13
comments: false
categories: hive, hadoop, R
---

### Summary

This post shows a simple, minimal example of using the
[R language](https://www.r-project.org/) with
[Apache Hive](https://hive.apache.org/) data warehouse.

### Introduction

Hive supports user defined aggregation functions (UDAF's) through custom programs
that process [`stdin` and
`stdout`](https://en.wikipedia.org/wiki/Standard_streams).
Hive sends each row of a table to the program via `stdin`. The program may
process the stream any way it wants. Then the program writes 
lines representing rows to `stdout`. Hive puts those lines together as a
table in the database. The model is flexible, so the program can write as many or as
few rows as it wants.

The `CLUSTER BY` part of the SQL below means that the stream Hive sends to
`stdin` will first be sorted based on the value of a column. This means
each unique value of that column will be processed by just one R script, so
we can process the entire group at a time. Processing large groups, ie.
1000's of rows at one time lets us write more efficient R code versus
processing one row at a time. A 
[follow up post]({{ site.baseurl }}{% post_url
2017-10-31-3-billion-rows-with-R %}) explains this idea further.

To run the code in this post, load up the `u_data` table of movie rankings following
the [Hive
documentation](https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-MovieLensUserRatings).

## Goal

I'm going to do the SQL equivalent of: 

```
SELECT userid, COUNT(*) as n
FROM u_data
GROUP BY userid
;
```

It's nice to first try something that SQL can do, because then we can verify
the answer. Of course the whole point of using R or any other program is to
go beyond what SQL can do.

## R script

The following R script essentially duplicates R's `table()` function
included with the `base` package. I wrote it in this way to emphasize the
split and apply operations.

Here's the `udaf.R` file:

```{R}
#!/usr/bin/env Rscript

# NOT stdin() - that's different ;)
infile = file("stdin")

tbl = read.table(infile)
s = split(tbl, tbl[, 1])

ans = lapply(s, function(ss){
    data.frame(ss[1, 1], nrow(ss))
})

ans = do.call(rbind, ans)

write.table(ans, stdout(), sep = "\t"
            , col.names = FALSE, row.names = FALSE)
```

This script loads everything from `stdin` straight into memory. It does not
stream. __This approach will fail for large enough data.__ It fails
because each individual R process may not be able to hold the subsets in
memory. Please see the [follow up post]({{ site.baseurl }}{% post_url
2017-10-31-3-billion-rows-with-R %}) to see how to do this properly using
streams in R.

## Development

Before running it in Hive it's a good idea to make sure the R script runs
locally. Test it on the actual data by downloading a small part of it from
Hive or HDFS. Then if the file is called `little.txt` you can run it on
the command line:

```{bash}
$ cat little.txt | Rscript udaf.R
```

If you see the table you expected printed to `stdout` then it worked. Be
happy. You can now run the `udaf.sql` script, comparing the results to the
initial query:

```{sql}
-- udaf.sql
DROP TABLE udaf
;

CREATE TABLE udaf (
  userid INT,
  count INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
;

add FILE udaf.R
;

INSERT OVERWRITE TABLE udaf
SELECT
TRANSFORM (userid)
USING "Rscript udaf.R"
AS (userid, count)
FROM (
    SELECT userid
    FROM u_data 
    CLUSTER BY userid
) AS tmp
;

SELECT *
FROM udaf
ORDER BY count DESC
LIMIT 10
;
```

# Debugging

If you don't have R installed on all the Hadoop worker nodes then you'll see an
error like this:
```
Caused by: java.io.IOException: Cannot run program "Rscript": error=2, No
such file or directory
```
The solution is simple; just install R on the worker nodes.

Scripts will fail. After unintentionally writing a few with bugs I wrote a
few very minimal scripts where I purposely injected bugs in various
locations and then reviewed the logs. Somewhere in the 1000's of lines of 
boilerplate you may find the root cause.

When the R script fails we need to look at the traceback so we can learn
something about why it failed. A couple blog post tutorials catch the error
in the script and write the traceback into the table. This technique works
with R, but mixes data with error logs. The system already logs `stderr`,
so we just need to find where to read those logs. Moreover, we can write to
`stderr` for logging purposes in a regular script that doesn't fail:

```{R}
# Helpful when grepping through the logs
writeLines("\n\n\nBEGIN R SCRIPT", stderr())
```

When I run the hive query I see a line like this indicating the YARN application ID:

```
Status: Running (Executing on YARN cluster with App id application_1480440170646_0140)
```

We can used this ID to inspect the logs:

```
$ yarn logs -applicationId application_1480440170646_0140 -log_files stderr | less
```

## Conclusion

The internet
has a few examples of how to [apply UDAF's with
Python](http://www.florianwilhelm.info/2016/10/python_udf_in_hive/), and
this inspired me to try the same thing with R. R works well for this
because a data frame is basically the same thing as a table.
