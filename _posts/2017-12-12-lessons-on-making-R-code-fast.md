---
layout: post
title: lessons on making R code fast
date: 2017-12-12 13:39
comments: false
categories: R, programming, parallel
---

These are some lessons I've learned as I attempt to accelerate R code.
It's all common knowledge, but sometimes common knowledge doesn't sink in
until you've made the mistakes yourself. Looking them over, they apply to
Numpy / Python as well.

## Lessons

Profile first, and then optimize the slow parts. After using R for several
years I can spot glaring errors, but beyond that my intuition is usually
wrong.

Check if someone has already written fast code that does what you want.

The speed of popular packages varies widely. For example,
[data.table](https://CRAN.R-project.org/package=data.table) is very fast.

When comparing different implementations, make sure they actually do the
same thing.

If you run out of memory then your program __will__ be slow, and it
probably won't run at all.

Non vectorized code __will__ be slow. Vectorized code is often fast, but
not always.

R can work surprisingly well on clusters / distributed systems.

Parallel execution is sometimes faster. Use `lapply` and `mapply` in your
code, so if you decide to go parallel then you can just drop in
`parallel::mclapply` or `parallel::mcmapply`.

Rewrite critical parts of the code in a compiled language like C if you
really need speed. This is particularly relevant for iterative computations
that can't be vectorized. Try other options first, because this makes the
code much more complex.
