---
layout: post
title: vectors to matrices and back
date: 2017-03-27 15:49
comments: false
categories: 
---

I've been playing around with data sets that won't fit in memory. One
experiment involves generating random data. Since it's so large it pays to
have everything as efficient as possible. 

Here's a trick to avoid copying
data that relies on the behavior of primitive replacement functions
modifying in place. In particular we're looking at the behavior of `dim`:

```
> `dim<-`
function (x, value)  .Primitive("dim<-")
```

The tricky way to create a matrix from a vector is to just set the
dimensions through `dim<-`, that is `dim()` on the left hand side of an
assignment operator. This is the same thing as [setting the
`shape`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.shape.html)
on a Numpy array in Python. A matrix (or higher dimensional array) is the
same as a vector in memory. They're both contiguous blocks of homogeneously
types data. The dimensions are metadata attached to this object.

```
> a = 1:10
> library(pryr)
> address(a)
[1] "0x2d37318"
> a
 [1]  1  2  3  4  5  6  7  8  9 10
> class(a)
[1] "integer"
> dim(a) = c(1, 10)
> a
     [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8] [,9] [,10]
[1,]    1    2    3    4    5    6    7    8    9    10
> class(a)
[1] "matrix"
> dim(a)
[1]  1 10
> address(a)
[1] "0x2d37318"
```

Since the memory address is the same we see this avoided a copy. The more
obvious way to instantiate a matrix is to call the `matrix()` function. I
prefer this because it's more expressive of what the programmer wishes to
happen: "make `b` a matrix with 1 row".

```
> b = 1:10
> address(b)
[1] "0x256d390"
> b = matrix(b, nrow = 1)
> b
     [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8] [,9] [,10]
[1,]    1    2    3    4    5    6    7    8    9    10
> address(b)
[1] "0x2dde6e8"
```

These addresses are different, so R copied the data. We know this program didn't
_need_ to copy data, but this copying is actually nice since this follows R's
functional programming model. Read more in Hadley Wickham's [Advanced R](http://adv-r.had.co.nz/memory.html#modification).
