---
layout: post
title: "Data Analysis Techniques"
date: 2014-04-10 20:03:11 -0700
comments: true
categories: data
---

I have little consistency when I do a data analysis project in R or Python. This occurs naturally because I'm a beginner, but it's also a nuisance. When I write a piece of code to answer some question about the data, I want to be able to easily access and replicate this.

## What I value in Data Analysis

1. **Accuracy** The analytic code should be correct and idiomatic.

2. **Repeatability** Code should be self contained and able to run. Right now I have a problem with this, since I'll often combine work that I have scripted with work from the interpreter. Many of my scripts are half baked. This leads to results which are not as easy to reproduce. Version control is important here as well.

3. **Persistency** Remote backups take care of this.

4. **Collaboration** I want to be able to easily share with other people, preferably without having to use email.

5. **Consistency** This is where I struggle. I've learned to create new folders for each project, but the structure of those folders is not consistent. Part of the problem is that I haven't found one that works particularly well. When in doubt, why not just do the simplest thing? Just have one folder. For small projects this makes sense, and simplifies things.

## A few different approaches

How do I achieve the desired outcomes above?

1. **Notebook Style** This involves using [Ipython Notebook](http://ipython.org/notebook.html) or R with [knitr](http://yihui.name/knitr/). Both of these are powerful tools, and should be the first thing that I reach for when I want to create a nicely formatted, presentable result.

2. **Scripts** Write all the analytic code in a single script. Mine usually aren't more than a couple hundred lines.

3. **Object Oriented** What if I had all the analysis packed into a Python object? This is a novel idea for me at the moment, and I've never tried it. It's a spin off of using the scripts above.

I like the scripting because it allows me to work in the shell, [Ipython](http://ipython.org/) interpreter, and Vim, my favorite text editor. This is a very powerful and efficient combination.

The code in a script or notebook will typically take 5-20 seconds to run, but some expensive operations can take minutes. I feel like there's no reason to wait unless I'm doing a heavy machine learning operation like [random forests](http://en.wikipedia.org/wiki/Random_forest) or neural nets. Maybe I could code the scripts in terms of what will be fast or slow. Python's [Pandas](http://pandas.pydata.org/) does that with the `@slow` decorator to mark slow unit tests. Perhaps I could incorporate that technique into my scripts.
