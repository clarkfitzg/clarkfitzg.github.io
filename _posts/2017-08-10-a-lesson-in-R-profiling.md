---
layout: post
title: a lesson in R profiling
date: 2017-08-10 16:52
comments: false
categories: R
---

{% include math.html %}

Punchline: Watch out for lazy evaluation and `.Primitive()` functions when
profiling R code.

While working on parallel R code, I wrote a [chunked version of the
covarance
function](https://gist.github.com/clarkfitzg/04c88efa3a426d08cd5618a01bc9356c).
The idea is to split the original problem into several chunks that can be
computed in parallel. This version is serial, but the idea is the same. The
actual work is done when the `cov()` function included with the `stats`
package is called on each chunk.

For an $$n \times p$$ matrix $$x$$ with $$n = 1,000,000$$ and $$p = 10$$ the
chunked version was about 3 times slower than just calling `cov()` by
itself. This surprised me, since I expected the overhead of breaking the
problem into chunks to be dominated by the actual computation inside calls
to `cov()`, thus making the chunked version only marginally slower then
`cov()` for sufficiently large $$n$$.

So I profiled it, and saw that nearly all of the time was spent
inside `is.data.frame()`:

```{r}
Rprof("cov_chunked.out")
replicate(10, cov_chunked(x))
Rprof(NULL)

summaryRprof("cov_chunked.out")

$by.self
                self.time self.pct total.time total.pct
"is.data.frame"      7.72    56.35       7.72     56.35
"cov"                5.98    43.65      13.70    100.00
```

How could `is.data.frame` be so slow? I looked at it quite
carefully, stepped through the debugger, traced it, counted all the calls,
but didn't understand. `is.data.frame` is a simple function that checks the
class, and takes less than 1 microsecond. Yet the profiler shows that each
call to `is.data.frame()` was taking hundreds of milliseconds, depending on
the problem size of $$n, p$$. This dependence on the problem size turned
out to be a major clue.

The following line was inside an lapply function:

```
cov(x[, index[[1]]], x[, index[[2]]])
```

Looking at the `cov()` function itself, the first uses of arguments `x` and
`y` are when it calls `is.data.frame()` on them. In this case `cov` called
`is.data.frame()` on `x[, index[[1]]]`, which was an unevaluated promise until that
point. The subset operator `[` was taking hundreds of milliseconds to
allocate memory and copy large chunks of `x`. R's copy on write model
doesn't apply here, because we didn't just pass in `x` alone.

The profiler should have showed me the time was actually spent within `[`.
But here's what we see at the R level:

```{r}
> `[`
.Primitive("[")
```

This means that `[` does absolutely everything in C, bypassing R code
completely. And it never showed up on the profiler.

Big thanks to Duncan Temple Lang for looking through this with me and figuring
it out~
