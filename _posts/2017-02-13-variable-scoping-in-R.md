---
layout: post
title: variable scoping in R
date: 2017-02-13 08:58
comments: false
categories: 
---

From the [R Language
Reference](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Search-path):

> Packages which have a namespace have a
> different search path. When a search for an R object is started from an
> object in such a package, the package itself is searched first, then its
> imports, then the base namespace and finally the global environment and the
> rest of the regular search path. The effect is that references to other
> objects in the same package will be resolved to the package, and objects
> cannot be masked by objects of the same name in the global environment or
> in other packages.

It's a little surprising that a package can look in _your_ global
environment. For example:

```
> library("findx")
> findx
function ()
x
<environment: namespace:findx>
> findx()
Error in findx() : object 'x' not found
> x = 100
> findx()
[1] 100
```

Writing code that looks up variables in the global namespace seems like a
very bad idea. Basically this shows that it's possible to shoot yourself in
the foot if you try hard enough.

Python won't let you:

```
In [1]: from findx import findx

In [2]: findx()
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-2-177571e7b710> in <module>()
----> 1 findx()

/home/clark/junkyard/findx.py in findx()
      1 def findx():
----> 2     return x

NameError: name 'x' is not defined

In [3]: x = 100

In [4]: findx()
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-4-177571e7b710> in <module>()
----> 1 findx()

/home/clark/junkyard/findx.py in findx()
      1 def findx():
----> 2     return x

NameError: name 'x' is not defined
```
