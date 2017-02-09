---
layout: post
title: variable assignments
date: 2017-02-09 10:05
comments: false
categories: 
---

## What are all the possible ways to do variable assignment in R?

I'll go from common to esoteric. Here's the one we're most familiar with:
```
x <- 10
```
This assigns `x` the value `10` in the current environment.
But in my own projects I usually write:
```
x = 10
```
There are three reasons for this.

1. Duncan Temple Lang does it this way, and he's the best R coder I
   know
2. Syntax more familiar when using multiple languages
3. One less character to write

We can also assign to the parent environment. This should be used judiciously,
because it breaks R's functional programming model. It comes in handy with
higher order functions. One can use a function to iterate through data,
updating shared state.
```
x <<- 10
```

These assignments also have the seldom used forms:
```
10 -> x
10 ->> x
```

As described in chapter 5 of John Chamber's book [Extending
R](https://www.amazon.com/Extending-Chapman-Hall-John-Chambers/dp/1498775713)
R has a functional form of assignment. Most other languages don't have
this.
```
x = matrix(0, nrow = 2, ncol = 2)

> x
     [,1] [,2]
[1,]    0    0
[2,]    0    0

diag(x) = 1

> x
     [,1] [,2]
[1,]    1    0
[2,]    0    1
```

We can 
assign a variable directly into an environment:
```
assign("x", 10)
```

Or we can do this in a more direct way:
```
.GlobalEnv$x = 10
```

### Summary

That's 8 different ways to do assignment. Of those, only `<-` and `=` are
very common.

### How about Python?

Here's the normal way:
```
x = 10
```

But the Python language is just a collection of dictionaries interacting in
a useful way. This allows us to do things like:
```
globals()["x"] = 10
```
