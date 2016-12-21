---
layout: post
title: first impressions of julia
date: 2016-12-21 11:25
comments: false
categories: programming, julia
---

Last week I tried the [Julia language](http://julialang.org/) for the first
time, and I'm very impressed. 

Over the past couple years I've been to several talks about Julia, but
never actually tried to use it. R and Python have always worked fine for my
applications. 

A couple things prevented me from jumping on board early.
As with any new language or technology, Julia was not that stable
initially. It sounds like 1.0 will be released next year, so this should
become less of a problem.
It also wasn't clear to what extent the language would support
vectorized operations. In R and Numpy users find it convenient to operate
on entire vectors and arrays at one time. Julia supports this:
```
julia> exp(1:5)  # Equivalent to [exp(x) for x in 1:5]
5-element Array{Float64,1}:
   2.71828
   7.38906
  20.0855
  54.5982
 148.413
```

One strength of Julia is that it's purpose built to use modern compiler
technology. In older languages this is added on after the fact, so it's
less natural.  Julia claims that the _syntax is familiar to users of other
technical computing environments_. I found this to be true.  Many of the
array functions even share the name as the equivalent ones in Numpy, like
`reshape`.  So I was able to move from R and Python to Julia and be
immediately productive with a numerical application (approximating log
likelihoods for high dimensional multivariate normal data).

If you're thinking about trying Julia, then do it.
Programming languages don't demand monogamy, and language wars are boring.
I would not hesitate to use Julia, especially for numeric / algorithmic
research applications where one wants to write fast code with a minimum of
fuss.

Big thanks to Professor Ethan Anderes at UC Davis for introducing the
language to me.
