---
layout: post
title: understanding R S4
date: 2018-06-12 08:53
comments: false
categories: R, object oriented, S4, software engineering
---

I've been reading John Chamber's book [Extending
R](https://www.crcpress.com/Extending-R/Chambers/p/book/9781498775717) and
it feels like another one of those things that I wish I would have read and
understood long ago. He argues for using S4 over S3 for more general software
engineering in R.

S4 is necessarily more complex than S3. This post is for me to gather my
thoughts and see if I understand it. There are copious amounts of
documentation out there.

## Exploring the space

Typically in R I use `ls()` to see which objects exist. The methods
package has better tools for this.

What classes does a package define?

```{r}
# Any package using S4
library(CodeDepends)
pkg = "package:CodeDepends"

getClasses(pkg)

# [1] "ScriptNodeInfo"  "Script"          "ScriptInfo"      "AnnotatedScript"
# [5] "ScriptNode"
```

What is the definition of the class, ie. the slots and the inheritance?

```{r}
getClass("AnnotatedScript")

# Class "AnnotatedScript" [package "CodeDepends"]
# 
# Slots:
# 
# Name:      .Data  location
# Class:      list character
# 
# Extends:
# Class "Script", directly
# Class "list", by class "Script", distance 2
# Class "vector", by class "Script", distance 3
```

What generic functions does the package use or define?

```{r}
getGenerics(pkg)

# An object of class "ObjectsWithPackage":
# 
# Object:  "[<-"  "["    "[[<-" "[["   "$<-"  "$"    "coerce"
# "getDependsThread"
# Package: "base" "base" "base" "base" "base" "base" "methods" "CodeDepends"
# 
# Object:  "getInputs"   "getVariables" "makeCallGraph" "names" "readScript"
# Package: "CodeDepends" "CodeDepends"  "CodeDepends"   "base"  "CodeDepends"
```

What methods have been defined for a particular generic function?

```{r}
methods(getInputs)

# [1] getInputs,ANY-method            getInputs,DynScript-method
# [3] getInputs,function-method       getInputs,Script-method
# [5] getInputs,ScriptNodeInfo-method getInputs,ScriptNode-method
```

What is the definition of a particular method?

```{r}
# Definition when calling getInputs(obj) where `obj` is of class function:

getMethod(getInputs, "function")

# Method Definition:
# 
# function (e, collector = inputCollector(), basedir = ".", reset = FALSE,
#     formulaInputs = FALSE, ...)
# {
# ...
```


## Basic Operations

Define new classes (usually done in a package):

```{r}

Schedule = setClass("Schedule",
    slots = c(code = "expression", evaluation = "data.frame"))

TaskSchedule = setClass("TaskSchedule",
    slots = c(transfer = "data.frame"),
    contains = "Schedule")

```

Now they show up here:

```{r}
"Schedule" %in% getClasses(globalenv())
```

Define a new generic function with a default method (usually done in a package):

```{r}

setGeneric("generateCode", function(Schedule, ...)
{
    Schedule@inCode
})

```


## Lazy evaluation

The methods dispatch on the class of the arguments, which requires
evaluating the arguments. Thus lazy evaluation is not possible for
these arguments.

```{r}
wont_eval = function(x, ...) NULL
wont_eval(stop())

# NULL

setGeneric("will_eval", function(x, ...) NULL)

will_eval(rnorm(1))

# NULL

will_eval(stop('first arg here'))

# Error in will_eval(stop("first arg here")) : first arg here
```
