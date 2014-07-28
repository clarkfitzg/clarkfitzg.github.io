---
layout: post
title: "Linux Utilities"
date: 2014-03-09 19:38:01 -0700
comments: true
categories: Linux Vim Pandas
---

I'm beginning to enjoy all the little utilities that make up Linux. It's been about 9 months since I was first exposed to Linux. I had the good fortune to have engineers teach me for a half day session. After that I was able to hit the ground running. Well, not exactly - More like crawling. Using the command line requires getting over the learning curve. And there's always more to learn.

Most recently I've been looking at the codebase for the excellent [pandas](http://pandas.pydata.org/) data analysis library in Python. It contains around 180K lines of Python code:

```
find . -name '*.py' | xargs wc -l  
180769 total
```

The above command looks in the current directory `.` to find all files whose name matches the regular expression *.py. This output is piped in as the argument to the `wc` wordcount program which counts the number of lines. I copied this pretty much directly from [Stack Overflow](http://stackoverflow.com/questions/1358540/how-to-count-all-the-lines-of-code-in-a-directory-recursively).

Another task has been running the built in test suite and examining the output. To do this you need to [redirect standard error](http://tldp.org/LDP/abs/html/io-redirection.html) `stderr` into a file so you can look at it.

```
nosetests pandas >> ../notes/Mar9_pandas.log 2>&1 
```

Then navigate to that log file and check it out with the `less` command.

At night I've been reading the book [The Pragmatic Programmer](http://pragprog.com/the-pragmatic-programmer). The authors compare building software to being a craftsman. The command line and text editor are like your bench and tools.
