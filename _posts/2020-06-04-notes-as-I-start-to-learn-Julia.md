---
layout: post
title: notes as I start to learn Julia
date: 2020-06-04 10:20
comments: false
categories: julia
---

I've been curious about the Julia programming language for many years, and have decided to sit down and actually start learning it.
These are my notes as I read the [official documentation](https://docs.julialang.org/en/v1/).

- Arithmetic overflows [wrap around](https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/#Overflow-behavior-1), like in C.
- What is a `do` block?
    The example in setting numeric precision appears to be making a temporary change in how a computation happens.
- Numeric literals for multiplication is nice syntax: `2x` rather than `2*x`.


## Limitations

Here's what I immediately noticed was missing.

- No [support for vi mode from the REPL](https://discourse.julialang.org/t/vim-mode-in-repl-command-line/9023), so quick experiments with expressions take longer and are more tedious than necessary.
- Cannot [access the source code from the REPL](https://github.com/JuliaLang/julia/issues/2625#issuecomment-498840808), so when I'm experimenting with minor variations of a function I have to take the extra step of saving them in a text file.


## `zero` function

Here are three ways to make a 64 bit floating point 0 in Julia: `zero(Float64)`, `0.0`, `Float64(0)`.
Naively, I would expect that the compiler would treat these expressions inside a function body exactly the same, but it doesn't.

```
function f1(x)
    x == zero(Float64)
    end

function f2(x)
    x == 0.0
    end

function f3(x)
    x == Float64(0)
    end
```

When I benchmark, for example, with `@benchmark f1(0.0)`, I find `f1(0.0)` is fast at 0.03 ns, while `f2(0.0)` and `f3(0.0)` both take around 18ns.
This means that the compiler treats `zero(Float64)` differently.
