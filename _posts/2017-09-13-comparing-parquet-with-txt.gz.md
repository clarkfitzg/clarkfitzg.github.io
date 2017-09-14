---
layout: post
title: comparing parquet with txt.gz
date: 2017-09-13 14:52
comments: false
categories: SQL, R, bigdata, benchmark
---

Summary:

Parquet was slightly faster than a compressed CSV file for a simple
Hive query.

## Background

Caltrans
Performance Management System [PeMS](http://pems.dot.ca.gov/)
makes traffic sensor observations publicly available.
I downloaded
a subset of their raw data- 300 days worth for one district. The downloaded
files came in compressed `txt.gz` files that occupy 24.1 GB on disk. There
were around 300 days, so 300 files, bringing the total dimensions up to 26
columns and 2.6 billion rows for the entire data set. It looks something
like:
```
time,station,flow, ...
10/02/2016 00:00:02,400001,0, ...
```
I wanted to do computations in R based on grouping by stations, rather than
by day as the files were currently grouped. Since the files were too large
to fit in memory I wrote a [basic
tool in R](https://gist.github.com/clarkfitzg/572037415c5150da143ae6bd0220c799)
to help with the splitting. This changed the grouping on the files from
by day to by station, which meant I could happily process each station file
alone in R. This simple single threaded R script took about 23 hours to run.

## Hive

After some [frustrations with
Spark](https://github.com/clarkfitzg/phd_research/blob/master/hadoop/notes.md)
I begin experimenting with [Apache Hive](https://hive.apache.org/) on our
modest 4 node cluster in the statistics department and
found that it made the above process smooth and easy. In particular I liked
the "schema on read" paradigm that let me use the `txt.gz` files in HDFS
from Hive without any complicated loading. The files just instantly became
a table. The R code to transform the daily files into the station files
became simpler SQL with higher level logic. Hive and 4 worker nodes
brought the 23 hours down to 1.5 hours.

[Apache Parquet](https://parquet.apache.org/), a binary columnar format,
seemed like it would further reduce overhead and help future work. I saved the data in
Parquet with Snappy compression, [bucketing the
data](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL+BucketedTables) as follows:

```{SQL}
SET hive.enforce.bucketing = true;

CREATE EXTERNAL TABLE pems_parquet (
    timeperiod STRING, station INT, flow INT
    -- ... more columns
)
CLUSTERED BY (station) INTO 256 BUCKETS
STORED AS PARQUET
LOCATION '/user/clarkf/pems_parquet_comp'
TBLPROPERTIES ("parquet.compression"="SNAPPY")
;
```

## Testing

I tested the speed of Parquet against the original gz compressed text
files, (hereafter `txt.gz`) with the following
simple query:

```{SQL}
SELECT station, MAX(flow1) FROM pems
GROUP BY station;
```

The buckets mean that the data in Parquet is already grouped by `station`.
Furthermore, only 2 out of 26 columns are required, so Parquet's columnar
storage should be a great advantage over the row based storage in `txt.gz`.
Thus I expected Parquet to be orders of magnitude faster than the `txt.gz`
files, but this wasn't the case.

This query took 78 seconds with Parquet, and 114 seconds with `txt.gz`.
So the `txt.gz` is only about 1.5 times slower
than Parquet. The sizes of the two tables on disk are about the same- 24.1
GB for the `txt.gz` and 25.1 GB for the Parquet (Uncompressed `txt` is 261
GB). 

## Final Thoughts

So what's going on? Was I wrong to expect better? Am I doing something
crazy? Seriously, if you have
an idea then please [let me know](https://twitter.com/clarkfitzg).

Parquet has many other things going for it. Storing metadata and column
type information will save gobs of time munging data. As a young, actively
developed project, I expect that we'll continue to see performance
improvements. But I was hoping for more.
