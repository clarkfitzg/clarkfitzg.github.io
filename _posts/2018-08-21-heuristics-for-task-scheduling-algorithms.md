---
layout: post
title: heuristics for task scheduling algorithms
date: 2018-08-21 13:19
comments: false
categories: parallel programming, task parallel
---

I've been reading Oliver Sinnen's book [Task Scheduling For Parallel
Systems](https://onlinelibrary.wiley.com/doi/book/10.1002/0470121173). The
idea of task scheduling is to make a program faster by running several
statements simultaneously. Here's a simple program:

```
x = foo()
y = bar()
foobar(x, y)
```

The computer can potentially run the first two lines at the same time and
then communicate to make `x` and `y` available to run the third line. This
is an example of a schedule, a mapping of expressions to processors. Task
scheduling generalizes this idea to arbitrary graphs of expressions. It's
NP hard.

## Types of Algorithms

Sinnen discusses three general heuristics for scheduling algorithms.

- __List scheduling__ is a greedy algorithm that assigns expressions to the
first ready worker.
- __Clustering__ groups computations on one worker to avoid the expense of
  transferring data.
- __Genetic algorithms__ start with random schedules and evolve them until
  they're good enough.

## Future Directions

While timing data analysis programs I've noticed that typically only a few
expressions take significant time. This suggests a different kind of
heuristic: Find an optimal schedule for the few long running expressions
and schedule everything else around that. I'll probably implement this in
the R [makeParallel
package](https://cran.r-project.org/package=makeParallel).
