---
layout: post
title: polyglot pipelines
date: 2018-04-27 08:23
comments: false
categories: R, Python, Unix, shell, bash, pipes
---

The [amazing Randy Lai](https://randycity.github.io/) recently posted a
[bug report](https://stat.ethz.ch/pipermail/r-devel/2018-April/075871.html)
on the [R-devel mailing
list](https://stat.ethz.ch/mailman/listinfo/r-devel). 
His example pipes text into an R process that executes the script in `test.R`.

```{bash}
$ echo "abc\nfoo" | R --slave -f test.R
```

R can run on the command line, read from `stdin` and write to `stdout`,
which means you can build shell pipelines with R. This can
be a nice way to combine several data processing steps in multiple
languages.

$ cat data.txt | R --slave -f step1.R
from Randy Lai

