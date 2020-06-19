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

## Stepping through each statement

```julia
using Debugger

f = function(x, y = 2)
    z = 3
    x + y + z
end

```
