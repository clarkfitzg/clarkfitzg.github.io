---
layout: post
title: converting cov2cor from R to julia
date: 2017-12-05 11:15
comments: false
categories: R, Julia, speed
---

{% include math.html %}

Recently I rewrote the `cov2cor()` function in R because I needed to use it
and I didn't know that it already existed in the `stats` package. I used a
`for` loop because this makes it obvious that the formula is correct. Let
$$X$$ be the covariance matrix. This formula transforms it to a correlation
matrix $$Y$$:

$$
    Y_{ij} = \frac{X_{ij}}{\sqrt{X_{ii} \cdot X_{jj}}}
$$

My version with the for loop in R took about 5 seconds to run on a $$1400
\times 1400$$ matrix. Below is the builtin R implementation for the vectorized version
in R. I've omitted error checking and modified the variable names for
consistency.

```{R}
cov2cor = function (X)
{
    n <- (d <- dim(X))[1L]
    d <- sqrt(1/diag(X))
    Y <- X
    Y[] <- d * X * rep(d, each = n)
    Y[cbind(1L:n, 1L:n)] <- 1
    Y
}
```

The vectorized version takes about 50 ms, so it's 100 times faster than my
naive `for` loop. The line `d * X * rep(d, each = n)` does the actual work
using [R's recycling
rules](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Recycling-rules).
Sometimes we can use R's column major storage to do even fancier
vectorization tricks, but it didn't matter here because this problem is
symmetric.  This code is reasonably fast, but it's not immediately obvious
that the result is the same as the formula given above.

I was curious about how much faster this could be, so I translated my naive
R `for` loop to Julia. At this point it became much less naive!  Professor
Ethan Anderes, our local Julia expert, kindly provided a few
variations that made it much faster through cache coherency and efficient
array initialization through `similar()`. Here's one Julia version:

```{julia}
function cov2cor(X) 
    d = 1./sqrt.(diag(X))
    Y = similar(X)   
    n = size(X,1) 
    @inbounds for col in 1:n 
        @simd for row in 1:col
            Y[row,col] = X[row,col] * d[row] * d[col]
        end 
    end 
    return Symmetric(Y)
end
```

This runs in about 2ms, making it 25x faster than R's vectorized version
and 2500x faster than an R `for` loop. I find Julia's two `for` loops:

```{julia}
for col in 1:n 
    for row in 1:col
        Y[row,col] = X[row,col] * d[row] * d[col]
    end 
end 
```

to be more clear than the equivalent line in R:

```{R}
Y[] <- d * X * rep(d, each = n)
```

It's more clear because I can recognize the correspondence to the formula
more quickly in the Julia version. I value clarity more than speed in most
cases. Here Julia provides both. One disadvantage is that I needed to know
Julia is column major in order to write the `for` loops in a cache friendly
way.

Thanks to Professor Anderes and the R code review group at the DSI for
showing interest in this.
