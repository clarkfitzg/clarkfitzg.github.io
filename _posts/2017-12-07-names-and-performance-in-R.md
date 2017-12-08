---
layout: post
title: names and performance in R
date: 2017-12-07 15:53
comments: false
categories: R, performance, tuning
---

Names decorating data structures are convenient. They allow us to write
more intelligible code, ie `people["Joe", "height"]`. But they can have
hidden performance costs.

```{R}
library(microbenchmark)

n <- 1e6L
l <- list(a = 1:n, b = 1:n)

# Super slow!
microbenchmark(out1 <- do.call(c, l), times = 10L)
```

It takes around 600 ms on my computer to combine two vectors of length 1
million. In contrast, if I write it in the following way it takes about 4 ms:

```{R}
# Super fast!
microbenchmark(out2 <- c(l[[1]], l[[2]]), times = 10L)

head(out1)
# a1 a2 a3 a4 a5 a6
#  1  2  3  4  5  6

head(out2)
# [1] 1 2 3 4 5 6
```

Both produce a vector of length 2 million by concatenating the two vectors
in a list. The only difference is that `do.call()` grabbed the names from
the containing list. This is convenient in most cases, but here performance
suffers by a factor of 150 times. Ouch.

```{R}
microbenchmark(out3 <- do.call(c, unname(l)), times = 10L)
```

This version is again fast, around 4 ms. Sometimes names hurt!
