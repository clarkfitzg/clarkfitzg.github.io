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
A debugger allows you to stop a program in the middle of execution and interact deeply with the software that you've written.
Debuggers validate your mental model of the program you've written, and your model of the language itself.
Duncan Temple Lang once remarked, "before you learn anything in a new programming language, you should learn the debugger."
I'm learning Julia now, so let's learn the debugger.


## Stepping through a program

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


## Stopping on error

It's often useful to stop and enter the debugger when an error occurs, so we can examine the state of the program under the exact conditions that produced the error.
Hopefully, this investigation will lead us to the root cause.

TODO: This would be more compelling if it was an actual bug that I ran into, vs. something contrived.
But it also has to be simple enough to be self contained.
I'm sure if I continue with these Project Euler problems I can get some nice examples.

```julia
squarelast = function(x)
    x[end]^2
end
```


