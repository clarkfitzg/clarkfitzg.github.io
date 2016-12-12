---
layout: post
title: gaussian process
date: 2016-12-12 10:54
comments: false
categories: statistics, theory, math
---

{% include math.html %}

Let $X_t$ be a random variable indexed by $t \in T$. Think of $t$ as being
time.
[Stochastic processes](https://en.wikipedia.org/wiki/Stochastic_process)
are sets of random variables of the form
$$
    \{ X_t : t \in T \}.
$$
For actual data we can only ever have one observation of each
$X_t$, which is why more assumptions are helpful.

### Special Cases

- If $X_t$ is vector valued then this is called a __random field__.
- If a linear combination of samples from a stochastic process is jointly
  normal then this is called a __Gaussian process__, or __Gaussian random
  field__ for the multivariate case.
- If $T$ is discrete and the value of $X_{t+1}$ only depends on $X_t$ then
  the process is a discrete time __Markov chain__.
