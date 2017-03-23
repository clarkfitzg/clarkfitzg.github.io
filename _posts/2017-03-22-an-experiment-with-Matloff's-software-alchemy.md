---
layout: post
title: an experiment with Matloff's software alchemy
date: 2017-03-22 17:02
comments: false
categories: 
---

{% include math.html %}

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

coef(fit)

# (Intercept)           x
#    1.001219    1.999820

vcov(fit)

#               (Intercept)             x
# (Intercept)  4.672165e-06 -6.674522e-07
# x           -6.674522e-07  1.213549e-07
```

Now let's try using the general chunk averaging function in Matloff's
[partools package](https://cran.r-project.org/package=partools).

```
library(partools)

cls = makeCluster(2)
setclsinfo(cls)

f = function(chunk) lm(y ~ x, data = chunk)

fit_ca = ca(cls, xy, f, coef, vcov)

# $thts
#      (Intercept)        x
# [1,]   0.9980718 2.000178
# [2,]   1.0043666 1.999463
# 
# $tht
# (Intercept)           x
#    1.001219    1.999820
# 
# $thtcov
#               (Intercept)             x
# (Intercept)  4.672163e-06 -6.674519e-07
# x           -6.674519e-07  1.213549e-07
```

The chunk averaging estimate of the covariance matrix of the coefficients differs
from the conventional estimates only in the 7th significant digit. So the
method works very well here.

As a side note I like expressing the computation as a function that
operates on a chunk, since this is conceptually how I think of this type
of parallel program. Python's [dask](http://dask.pydata.org/en/latest/spec.html)
library uses a similar model with callables. That was this line:
```
f = function(chunk) lm(y ~ x, data = chunk)
```

## Non IID data

What happens when we violate the assumption that the chunks consist of
iid observations? For example, sorted data is not iid. Below I'll take that
a bit further and put the relatively small and large values of $$y$$ in
separate chunks. This should result in different (and incorrect) intercept estimates across
the two chunks.

```
xy2 = xy[order(xy$x, xy$y), ]
low = rep(rep(c(TRUE, FALSE), each = 50000), 10)
xy3 = rbind(xy2[low, ], xy2[!low, ])

fit_sorted = ca(cls, xy3, f, coef, vcov)

# $thts
#      (Intercept)        x
# [1,]   0.2022849 1.999896
# [2,]   1.8001534 1.999745
# 
# $tht
# (Intercept)           x
#    1.001219    1.999820
# 
# $thtcov
#               (Intercept)             x
# (Intercept)  1.696553e-06 -2.423648e-07
# x           -2.423648e-07  4.406632e-08
```

Indeed the intercept estimates for the two chunks are different from the
correct value of 1. One is around 0.2 and another 1.8 as seen in the values
of `(Intercept)` in `$thts`, which presuambly stands for $$\theta$$'s.  The
average `$tht` is still correct because of symmetry. 

The estimated covariances for $$\theta$$ in this new averaged model are
smaller than the true ones by a constant factor. This is because the data
in each chunk had less variance than before since the noise effectively
came from just one half of a normal distribution.

```
vcov(fit) / fit_sorted$thtcov

#             (Intercept)        x
# (Intercept)    2.753916 2.753916
# x              2.753916 2.753916
```

This suggests a common sense way to build confidence when applying 
the software alchemy approach: compare the empirical covariance of the
$$\hat{\theta}_i$$'s (`$thts`) with the estimated covariance matrix
$$Var(\tilde{\theta})$$ (`$thtcov`). For this averaging based
approach one would expect the ratio $$\frac{Var(\hat{\theta}_i)}{Var(\tilde{\theta})$$ to be 
roughly in the neighborhood of $k$, the number of chunks.

This was satisfied with iid samples and 2 chunks. These values are "close
enough" to 2. They're not especially close because we're estimating covariance
with only 2 samples, which won't be too acccurate.

```
cov(fit_ca$thts) / fit_ca$thtcov

#             (Intercept)        x
# (Intercept)    4.240463 3.369001
# x              3.369001 2.103070
```

Bumping up the number of chunks / workers to 20 increases the accuracy of the
empirical estimate of $$Var(\theta_i)$$, so the ratio becomes relatively closer to 20.
Again this gives us confidence.

```
cls = makeCluster(20)
setclsinfo(cls)

fit_ca20 = ca(cls, xy, f, coef, vcov)

cov(fit_ca20$thts) / fit_ca20$thtcov

#             (Intercept)        x
# (Intercept)    19.09641 18.03746
# x              18.03746 16.78620
```

However, consider the case where the data were not randomly assigned to the chunks:

```
cov(fit_sorted$thts) / fit_sorted$thtcov

#             (Intercept)           x
# (Intercept) 752461.9508 499.3144833
# x              499.3145   0.2603325
```

These numbers are orders of magnitude away from $k = 2$. This tells us
that the data weren't iid in the chunks or there was some other serious
issue with the actual versus the expected variance of the estimate
$$\hat{\theta}$$.
