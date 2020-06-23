---
layout: post
title: intro to Julia's Debugger
date: 2020-06-19 08:34
comments: false
categories: julia, debugging, software
---

This post demonstrates Julia's [Debugger](https://github.com/JuliaDebug/Debugger.jl) through some simple examples.

## Introduction

Learning how to use a debugger was an important milestone in my growth as a programmer.
I thought I was doing fine without it, but I just didn't know what I was missing.
A debugger allows you to stop a program in the middle of execution and interact directly with the software that you've written.
Debuggers validate your mental model of the program you've written, and your model of the language itself.
Duncan Temple Lang once remarked, "before you learn anything in a new programming language, you should learn the debugger."

What follows is a brief, self contained, introduction to Julia's debugger.
You may also enjoy Norm Matloff's more [general resources on debugging](http://heather.cs.ucdavis.edu/~matloff/debug.html).


## Stepping Through a Program

We start by loading Debugger and defining a simple function, `f`.
```julia
using Debugger

f = function(x, y = 2)
    z = 3
    x + y + z
end
```

We can enter the debugger by prefacing a function call with the aptly named macro `@enter`.
```julia
@enter f(1)
```

The debugger displays the following output.
```julia
In #1(x, y) at REPL[1]:1
 1  f = function(x, y = 2)
 2      z = 3
>3      x + y + z
 4  en

About to run: (+)(1, 2, 3)
1|debug>
```

This means that the current program state is paused inside the call `f(1)`.
The `>` symbol in front of line 3 means the debugger is ready to run line 3: `x + y + z`.
The prompt has changed to `1|debug>`, since we are in the debugger, not the Julia REPL.

From the debug prompt, we can enter any valid Debugger commands.
Type `?` followed by enter to see the possible commands.

```julia
1|debug> ?
  Debugger commands
  ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

  Below, square brackets denote optional arguments.

  Misc:
  - o: open the current line in an editor
  - q: quit the debugger, returning nothing
  ... (and many more)
```

Let's start by looking at the variables in our current frame.
These are the local variables inside the function.
We expect to see `x, y, z` bound to `1, 2, 3`.
```julia
1|debug> fr
[1] #1(x, y) at REPL[1]:1
  | x::Int64 = 1
  | y::Int64 = 2
  | z::Int64 = 3
```

Indeed they are.
To evaluate any Julia expression, we type `` ` `` (a backtick) and Debugger gives us a Julia prompt.
We can call functions on the local variables _based on their current state in the function execution_.
```julia
1|julia> 2*x
2
```

We can also manipulate the state of the computation.
Suppose we would like to see what happens in the rest of the function if `x = 2.0`.
```julia
1|julia> x = 2.0
2.0
```

Type Ctrl+C to exit the Julia prompt and return to the debug prompt.
```julia
1|julia> ^C

1|debug>
```

Inspecting the variables in our current frame shows the new value for `x`.
```julia
1|debug> fr
[1] #1(x, y) at REPL[1]:1
  | x::Float64 = 2.0
  | y::Int64 = 2
  | z::Int64 = 3
```

`n` steps to the next line in the function body, which is the implicit `return` statement.
The call returns `2.0 + 2 + 3 = 7.0`.
```julia
1|debug> n
In #1(x, y) at REPL[1]:1
 1  f = function(x, y = 2)
 2      z = 3
>3      x + y + z
 4  en

About to run: return 7.0
```

`c` continues execution until a breakpoint is hit.
We didn't add any breakpoints, and we're already at the `return` statement anyways, so the call returns and we exit the debugger, returning to the main Julia REPL.
```julia
1|debug> c
7.0

julia>
```

That's it for the basic introduction.
The next example contains an actual bug.


## Stopping on Error

It's often useful to stop and enter the debugger when an error occurs, so we can examine the state of the program under the exact conditions that produced the error.
We do this with Debugger by calling `break_on(:error)`, then `@run` in front of the expression that produces the error.
Hopefully, this investigation will lead us to the root cause.

The following code calculates and prints `2*3 + 4`, but it contains two bugs.

```julia
axpy1 = function(a, x, y)
    ax + y
end

f1 = function()
    a = 2
    x = 3
    y = 4
    println("If a = $a, x = $x, y = $y, then ax + y = $(axpy1(x, y, a))")
end
```

When we call `f1()`, we see the following error message:
```julia
julia> f1()
ERROR: UndefVarError: ax not defined
Stacktrace:
 [1] (::var"#5#6")(::Int64, ::Int64, ::Int64) at ./REPL[45]:2
 [2] (::var"#9#10")() at ./REPL[48]:5
 [3] top-level scope at REPL[49]:1
```

We don't need debugging to fix this error.
This error message tells us exactly what the problem is: we never defined the variable `ax`.
Our program is simple, and the stack trace only contains three frames, so if we have the correct mental model of how the language works, then we can reason through it to fix the error.

Debugging becomes truly useful when the problem is __not__ obvious.
The error message may be uninformative, the program may be complex, and the stack trace may contain more frames than you can fit in your head.
If you hit an error, and you don't know what's wrong, then run the same code through the debugger, as follows.
```julia
julia> break_on(:error)

julia> @run f1()
Breaking for error:
ERROR: UndefVarError: ax not defined
Stacktrace:
 [1] (::var"#11#12")(::Int64, ::Int64, ::Int64) at REPL[52]:2
 [2] (::var"#13#14")() at REPL[53]:5

In #11(a, x, y) at REPL[52]:1
 1  axpy1 = function(a, x, y)
>2      ax + y
 3  en

About to run: (+)(Main.ax, 2)
1|debug>
```

We are now in the debugger prompt, _inside the call to `axpy1()`,_ so we can enter any of the debugger commands.
The error message said variable `ax` is not present.
What variables are present?
Let's see.
```julia
1|debug> fr
[1] #11(a, x, y) at REPL[52]:1
  | a::Int64 = 3
  | x::Int64 = 4
  | y::Int64 = 2
```

We have `a`, `x`, and `y`, but no `ax`.
Ah, of course: we should have written `a*x` instead of `ax`.
Let's fix this bug:
```julia
axpy2 = function(a, x, y)
    a*x + y
end

f2 = function()
    a = 2
    x = 3
    y = 4
    println("If a = $a, x = $x, y = $y, then ax + y = $(axpy2(x, y, a))")
end
```

<!--
Julia allows [juxtaposed expressions like `10x`](https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/#man-numeric-literal-coefficients-1), but no sane programming language can know that `ax` should actually mean `a*x`, even if the mathematical notation was perfectly clear to the human reader.
-->

We call it as follows:
```julia
julia> f2()
If a = 2, x = 3, y = 4, then ax + y = 14
```

That's not right.
`2 * 3 + 4 = 10`, not `14`.
Indeed, this is an altogether more troubling class of bug: one that executes perfectly fine, but produces the wrong answer. 😭
Let's use another debugging technique, breakpoints, to see what went wrong.


## Setting Breakpoints
