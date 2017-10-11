---
layout: post
title: missing arguments in parsed R expressions
date: 2017-10-11 09:12
comments: false
categories: R, metaprogramming
---

R allows the programmer to manipulate code just like any other object, aka
'computing on the language'.

Consider the following R code:

```{R}

e = quote(x[, 10])

```

`e` is a parsed expression containing the code needed to select the 10th
column of a data frame or matrix `x`. If we have such a matrix it can be
evaluated:

```{R}

x = matrix(1:10, nrow = 1)

eval(e)  # returns 10

```

We can manually traverse the parse tree in `e` just by indexing into it:

```{R}

> e[[1]]
`[`
> e[[2]]
x
> e[[3]]

> e[[4]]
[1] 10

```

`e[[3]]` is the interesting element here. It represents a missing argument.
Although we can assign it to a variable we can't treat it as a normal
object. More specifically, we can't pass it to any functions that will
evaluate it in the standard way.

```{R}

> e3 = e[[3]]
> e3
Error: argument "e3" is missing, with no default
> class(e3)
Error: argument "e3" is missing, with no default
```

However, we can check whether it is missing:

```{R}
> missing(e3)
[1] TRUE

```

Lately I've been traversing parse trees in R, and I used the `missing()`
function to make the tree traversal more robust by handling this special
case.
