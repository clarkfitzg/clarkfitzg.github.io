---
layout: post
title: using global variables with multicore
date: 2018-02-20 09:48
comments: false
categories: R, parallel programming, metaprogramming
---

It's generally considered poor style to use global variables inside
functions. For example:

```{R}

n = 1e8
x = rnorm(n)

# explicitly uses a global variable. Good.
f = function(.x = x) mean(.x)

# implicitly uses a global variable. Bad.
f_global = function() mean(x)

# They do the same thing.
f_global() == f()

```

But if the data we're computing on is very large then it can be expensive
to transfer the data. The following code creates a new forked R process
where the variable `x` is defined, so that both `f()` and `f_global()` work.

```{R}
library(parallel)

cls = makeCluster(1L, "FORK")

calls = parse(text = "
    f()
    f_global()
    clusterCall(cls, f)
    clusterCall(cls, f, x)
    clusterCall(cls, f_global)
")

times = sapply(calls, function(expr) 
    system.time(eval(expr), gcFirst = FALSE)["elapsed"]
)

dotchart(times, calls, xlim = c(0, max(times)), xlab = "seconds elapsed")
```


```
> clusterCall
function (cl = NULL, fun, ...)
{
    cl <- defaultCluster(cl)
    for (i in seq_along(cl)) sendCall(cl[[i]], fun, list(...))
    checkForRemoteErrors(lapply(cl, recvResult))
}
<bytecode: 0x405ae38>
<environment: namespace:parallel>
```

This code demonstrates how we can use R's idiomatic style even for
metaprogramming.
