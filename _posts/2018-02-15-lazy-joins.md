---
layout: post
title: lazy joins
date: 2018-02-15 16:10
comments: false
categories: R, databases
---

A [view](https://en.wikipedia.org/wiki/View_(SQL)) in a database is the
result of some fixed query. Views allow the user to work at a
higher level of denormalized, more easily digested data. They don't require
intimate knowledge of the underlying physical schema of the database. So
views are very nice for statisticians and data analysts.

The R programming language doesn't have the notion of a view in the
database sense. It just has data frames residing in memory. Calling
`merge(df1, df2)` will create a new data frame by performing a natural
join. This is fine if both data frames are small, but can exceed available memory
once they become large, causing the operation to fail.

We can make something like a view in R by creating two intermediate vectors
to represent the join. The intermediate vectors of indices describe which
rows to bring from each table to make a join.
