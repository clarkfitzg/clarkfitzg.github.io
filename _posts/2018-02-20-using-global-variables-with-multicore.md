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

# implicitly uses a global variable. Bad.
f_global = function() mean(x)

# explicitly uses a global variable. Acceptable.
f = function(.x = x) mean(.x)

# They do the same thing.
f_global() == f()

```

But if the data we're computing on is very large then it can be expensive
to transfer the data, so we want to avoid this. The following code creates
a new forked R process where the variable `x` is defined, so that both
`f()` and `f_global()` work.

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

png("../assets/2018-02-20_call_times_in_cluster.png")
dotchart(times, calls, xlim = c(0, max(times)), xlab = "seconds elapsed")
dev.off()
```

When we call `clusterCall` with `x` as an argument the master process
serializes `x` to the worker. We can tell none of the other versions of the
code transfer `x` because the other times are all the same.

![]({{ site.url }}/assets/2018-02-20_call_times_in_cluster.png)

This particular machine takes around 1 second
to transfer an object `x` which takes up about 1 GB of memory, for a speed
on the order of 1 GB/sec.  Running this same code with a remote worker
exacerbates the problem, because the network must transfer the data.

If we look at the source for R's parallel package we see that the
additional arguments are gathered up into `list(...)` and sent to the
worker through `sendCall()` which calls `postNode()` which calls
`sendData()` which calls `sendData.SOCKnode()` which finally calls
`serialize()` to transfer the data.

```
sendData.SOCKnode <- function(node, data) serialize(data, node$con)
```

## Thoughts

On a side note, I was pleased that `dotchart()` accepted the code
expressions. It shows we can use normal R style with code objects. Just be
careful.

I was a little surprised that `clusterCall(cls, f)` didn't transfer `x`.
But maybe I shouldn't be surprised, because to know that `x` "should" be
transferred `clusterCall` would have had to inspect the signature for `f`
and analyze the arguments.
