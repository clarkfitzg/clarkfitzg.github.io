---
layout: post
title: string formatting with files in bash
date: 2018-09-21 11:07
comments: false
categories: bash, strings, formatting, automation, printf, echo
---

## The problem

I need to generate a file with very simple structure, just a LaTeX file with a few `include` statements.
Until today, I was copying a template and manually changing it.
This was slow, redundant, and error prone.
I decided to just generate the files from the template instead.
I wanted to use bash for this rather than a scripting language, because then it will connect better with the whole GNU Make workflow of the project.

## The solution

I started by putting the template in the Makefile and using `echo`, as I normally do.
This gave me some problems, so I started looking into alternatives that would let me keep the template as a separate file.
Most people recommend `printf` as a more robust alternative.
Then the problem was, how to pass `printf` the `FORMAT` argument from a file?
That's what `xargs` does.

Here's a simple example.
First you'll need a `format.txt` file, or whatever you choose to call it.

```
$ printf "%%s and %%s\n" > format.txt                                                 
```

The `%%` just escapes the special character `%` for `printf`:

```
$ cat format.txt
%s and %s
```

Then we can use it as follows:

```
$ cat format.txt | xargs -0 -I{} printf {} A B
A and B
```

We read this command as `printf <contents of format.txt> A B`.
`xargs` always makes me do some mental gymnastics.
The `-0` flag prevents `xargs` from messing with the actual contents, i.e. removing whitespace.
`-I{}` allows me to take the text and pass it as the first argument with `printf {} ...`.
Otherwise it would be the last argument.

Here's how I actually use it in my Makefile:

```
%.tex: tex/%.tex texformat.txt preamble.tex
	cat texformat.txt | xargs -0 -I{} printf {} $< $< > $@
```
