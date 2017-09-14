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

Caltrans Performance Management System [PeMS](http://pems.dot.ca.gov/)
makes traffic sensor observations publicly available.  I downloaded a
subset of their raw data- 300 days worth for one district. The downloaded
files came in compressed text files (hereafter `txt.gz`) that occupy 24.1
GB on disk. There were around 300 days, so 300 files, bringing the total
dimensions up to 26 columns and 2.6 billion rows for the entire data set.
It's fairly sparse, with maybe 80% of the values missing. But it is a real
data set found out in the wild, rather than a simulation.  With spaces for
readability it looks something like:

```
time,                   station,    flow,   occupancy ...
10/02/2016 00:00:02,    400001,     0,      0.015 ...
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
from Hive without any complicated loading. The files in HDFS just instantly became
a table that could be queried. The R code to transform the daily files into the station files
became simpler SQL with higher level logic. Hive with 4 worker nodes
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

I tested the speed of Parquet against `txt.gz` with the following
simple query:

```{SQL}
SELECT station, MAX(flow) FROM pems
GROUP BY station;
```

The buckets mean that the data in Parquet is already grouped by `station`.
Furthermore, only 2 out of 26 columns are required, so Parquet's columnar
storage should be a great advantage over the row based storage in `txt.gz`.
Thus I expected Parquet to be orders of magnitude faster than the `txt.gz`
files, but this wasn't the case.

This query took 78 seconds with Parquet, and 114 seconds with `txt.gz`.
The sizes of the two tables on disk are about the same- 24.1 GB for the
`txt.gz` and 25.1 GB for the Parquet. The uncompressed `txt` performed much
worse; it's 261 GB on disk and the same query took 420 seconds. 

## Final Thoughts

The goal is to have a data format that is both small and fast.
`txt.gz` is marginally smaller and only about 1.5 times slower
than Parquet. Uncompressed `txt` is about 10 times larger and 5 times
slower than Parquet.  Of course this is just one experiment, and it doesn't
show that the formats are equivalent. Some aspects of this data set 
certainly influence performance, such as the sparsity pattern and the
floats which are represented by only a couple ASCII characters.

This result does show that simple
compressed text _might_ perform close to a more specialized binary format,
so it shouldn't be dismissed outright.
So what's going on? Was I wrong to expect better? Am I doing something
crazy? Seriously, if you have
an idea then please [let me know](https://twitter.com/clarkfitzg).
Code can be [found
here](https://github.com/clarkfitzg/phd_research/tree/master/hadoop).

Parquet has many other things going for it. Storing metadata and column
type information will save huge amounts of time munging data by removing
a whole class of bugs. The related [Apache
Arrow](https://arrow.apache.org/) project looks very promising to create
low overhead, in memory representations from Parquet. As a young, actively
developed project, I expect that we'll continue to see Parquet performance
improvements. But I was hoping for more.
