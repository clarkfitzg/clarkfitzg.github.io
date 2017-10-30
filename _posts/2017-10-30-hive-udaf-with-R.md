---
layout: post
title: hive udaf with R
date: 2017-10-30 14:13
comments: false
categories: hive, hadoop, R
---

This post shows a simple, minimal example of using R with
[Apache Hive](https://hive.apache.org/) data warehouse.

Hive supports user defined aggregation functions (UDAF's) through custom programs
that process [`stdin` and
`stdout`](https://en.wikipedia.org/wiki/Standard_streams). The internet
has a few examples of how to [apply UDAF's with
Python](http://www.florianwilhelm.info/2016/10/python_udf_in_hive/).

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

It's nice to first do something that SQL can do, because then we can verify
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
memory. Maybe in a follow on post I'll show how to [do this in a scalable
and efficient way](https://github.com/clarkfitzg/phd_research/blob/master/analysis/pems/hadoop/piecewise_fd.R)
using streams in R.

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
locations and then reviewed the logs. This is helpful to figure out what is
happening.

When the R script fails we need to look at the traceback so we can learn
something about why it failed. A couple blog post tutorials catch the error
in the script and write the traceback into the table. This technique works
with R, but mixes data with error logs. The system already logs `stderr`,
so we just need to find where to read those logs. Moreover, we can write to
`stderr` for logging purposes in a regular script that doesn't fail.

When I run the hive query I see a line like this indicating the YARN application ID:

```
Status: Running (Executing on YARN cluster with App id application_1480440170646_0140)
```

We can used this ID to inspect the logs:

```
$ yarn logs -applicationId application_1480440170646_0140 -log_files stderr | less
```
