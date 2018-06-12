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
thoughts and see if I understand it.

## Exploring the space

Typically in R I use `ls()` to see which objects exist. The methods
package has better tools for this.

Show existing classes:

```{r}
# Any package using S4
library(CodeDepends)
pkg = "package:CodeDepends"

getClasses(pkg)

# [1] "ScriptNodeInfo"  "Script"          "ScriptInfo"      "AnnotatedScript"
# [5] "ScriptNode"
```

Inspect class definition, ie. the slots:

```{r}
getClass("ScriptNodeInfo")

# Class "ScriptNodeInfo" [package "CodeDepends"]
# 
# Slots:
# 
# Name:        files     strings   libraries      inputs     outputs
# updates
# Class:   character   character   character   character   character
# character
# 
# Name:    functions     removes  nsevalVars sideEffects        code
# Class:     logical   character   character   character         ANY

```

Show existing generic functions:

```{r}
getGenerics()

An object of class "ObjectsWithPackage":

Object:  "^"    "<"    "<="   "=="   ">"    ">="   "|"    "-"    "!="   
Package: "base" "base" "base" "base" "base" "base" "base" "base" "base"
```

See what 


```{r}


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
evaluating the arguments. Thus lazy evaluation should not be possible for
these arguments.

```{r}

stand

```


