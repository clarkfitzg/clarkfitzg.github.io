---
layout: post
title: are apply functions faster than for loops?
date: 2017-11-06 13:28
comments: false
categories: R, performance
---

Are apply style function in R, say `sapply()` any faster than `for` loops
in R? We can gain some insight using the `microbenchmark` package.

## Rules of thumb

Write vectorized R code when possible, ie. `y <- f(x)`. This 
single line of code totally expresses the desired computation.

If the function doesn't operate on vectors or the data is a list then use a
higher order function such as `sapply`, `lapply`, etc. These typically
capture the intent of the code more succinctly than a for loop. I like them
because they're easier to parallelize.

Below is a little experiment:

```{R}

library(microbenchmark)

n = 10000L
x = seq(from = 0, to = pi, length.out = n)

f = function(x)
{
    out = log(0.43 * x + 1)
    out = exp(x)
    x
}


baseline = median(microbenchmark(

    y <- f(x)

)$time)


apply_time = median(microbenchmark(

    y2 <- sapply(x, f)

)$time)


for_time = median(microbenchmark({

y3 <- vector(mode = "list", length = n)
for(i in 1:n){
    y3[[i]] = f(x[i])
}
y3 <- as.numeric(y3)

})$time)


apply_time / baseline

for_time / baseline

for_time / apply_time

```

Note the complexity of the implementations as measured by lines of code.
The vectorized and `sapply()` versions take only 1 line, while the
`for()` loop uses 4 or 5 lines.

## Results

The `sapply()` was faster than the `for()` loop, but how much faster
depends on the values of `n`.

For `n = 100` the `sapply()` is 15 times slower than the vectorized
version, and the `for()` is 23 times slower than the `sapply()`!

For `n = 10000` the `sapply()` is 19 times slower than the vectorized
version, and the `for()` is 1.16 times slower than the `sapply()`.
In other words, as the number of elements grows much past 1000 we see less
speed benefits from choosing `sapply()` over `for()`. Choose `sapply()` for
other reasons.

Main Conclusion: Both `sapply()` and `for()` loops are much slower than
vectorized code. 
