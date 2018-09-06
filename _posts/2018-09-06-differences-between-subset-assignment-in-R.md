---
layout: post
title: differences between subset assignment in R
date: 2018-09-06 10:50
comments: false
categories: R, subset
---

Today I used a data frame where one column was a list
consisting so that each row could contain its own list. I used this nesting
approach so that I could add arbitrary elements to each row.

I ran into a difference in the assignment operators `$<-` and `[[<-` that I
didn't expect. There are multiple ways to `[[` and `$` to select the
same data, but they do different things when assigning back into them.
Here's what I mean:

```{r}
d = data.frame(a = 1:2)
d$b = list(list(foo = 10), list(foo = 20))

d$b
# [[1]]
# [[1]]$foo
# [1] 10
# 
# [[2]]
# [[2]]$foo
# [1] 20
```

We can use the list method to extract.

```{r}
d[["b"]][[1]][["foo"]]
# [1] 10
```

Or we can use the data frame method to extract. They both give the same
result.

```{r}
d[, "b"][[1]][["foo"]]
# [1] 10
```

Assigning with the `[[<-` does what I expect; it replaces the 10 with the
new value and keeps all the structure.

```{r}
d[["b"]][[1]][["foo"]]

d$b
# [[1]]
# [[1]]$foo
# [1] 10
# 
# [[1]]$bar
# [1] 5
# 
# 
# [[2]]
# [[2]]$foo
# [1] 20
```

If we use the data frame `[<-` to do the assignment then R warns us.

```{r}
d[, "b"][[1]][["foobar"]] = TRUE
Warning message:
In `[<-.data.frame`(`*tmp*`, , "b", value = list(list(foo = 10,  :
  provided 2 variables to replace 1 variables

```

We lost the structure and the data. This is not what I wanted.

```{r}
d$b
# $foo
# [1] 10
# 
# $foobar
# [1] TRUE
```

## Conclusion

Check your intuition when using lists inside data frames, they may not do
what you expect.

As another example, here's how to NOT make the same list as the original `d`:

```{r}
d2 = data.frame(a = 1:2, b = list(list(foo = 10), list(foo = 20)))
d2
#   a b.foo b.foo.1
# 1 1    10      20
# 2 2    10      20
```

If I'm missing some higher unifying logic with all this then please let me
know and I'll update this post.
