---
layout: post
title: an experiment with Matloff's software alchemy
date: 2017-03-22 17:02
comments: false
categories: 
---

Norm Matloff describes [Software Alchemy](https://arxiv.org/abs/1409.5827)
as the process of transforming a non embarrassingly parallel problem into
an embarrasingly parallel one through the use of statistical averaging.
Let $$n$$ be the number of data points, $$r$$ be the number of chunks and
$$n_i$$ be the number of data points randomly assigned to the $$i_th$$ chunk. Let
$$\hat{\theta}_i$$ be the estimator fitted to the $$i_th$$ chunk.  Then the
weighted average of these estimators forms the chunk average estimator:

$$
\tilde{\theta} = \sum_{i = 1}^r \frac{n_i}{n} \hat{\theta}_i
$$

This is asymptotically equivalent to $$\hat{\theta}$$, the estimate
of the parameter on the whole data set.

Let's experiment with this idea using a simple linear model $$y = 1 + 2x +
\epsilon$$.

The set up:
```

set.seed(37)
n = 1e6
x = rep(1:10, times = n / 10)
y = 1 + 2*x + rnorm(n)
xy = data.frame(x, y)

```

The ordinary OLS estimates:

```

fit = lm(y ~ x, data=xy)

> coef(fit)
(Intercept)           x
   1.001219    1.999820

> vcov(fit)
              (Intercept)             x
(Intercept)  4.672165e-06 -6.674522e-07
x           -6.674522e-07  1.213549e-07

```

Now let's try using the general chunk averaging function in Matloff's
[partools package](https://cran.r-project.org/package=partools).

```

library(partools)

cls = makeCluster(2)
setclsinfo(cls)

f = function(chunk) lm(y ~ x, data = chunk)

> ca(cls, xy, f, coef, vcov)
$thts
     (Intercept)        x
[1,]   0.9980718 2.000178
[2,]   1.0043666 1.999463

$tht
(Intercept)           x
   1.001219    1.999820

$thtcov
              (Intercept)             x
(Intercept)  4.672163e-06 -6.674519e-07
x           -6.674519e-07  1.213549e-07

```

