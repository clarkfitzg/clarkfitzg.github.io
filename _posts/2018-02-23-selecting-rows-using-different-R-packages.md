---
layout: post
title: selecting rows using different R packages
date: 2018-02-23 11:16
comments: false
categories: R, data.table, dplyr, data frame, data analysis
---

There are three popular ways to manipulate and analyze data frames in R:

- [base R](https://www.r-project.org/)
- [data.table](https://github.com/Rdatatable/data.table/wiki)
- [dplyr](http://dplyr.tidyverse.org/)

These packages are not mutually exclusive, ie one might mix two of them. We
can refer to them as domain specific languages (DSL)'s because they all offer distinct syntax
to perform operations that resemble SQL type queries on tables. They go
beyond SQL since they support general R functions. 

I'm interested in these DSL's for the purpose of code analysis and code
transformations, for example creating parallel code from serial. To analyze the
code we need to precisely understand the semantics when each function uses
[nonstandard
evaluation](http://adv-r.had.co.nz/Computing-on-the-language.html) (NSE).

This post shows all the different common ways to do a basic row selection
operation using these three packages. If I missed any please [let me
know](https://twitter.com/clarkfitzg). I borrowed the example from the
[dplyr
documentation](https://cran.r-project.org/web/packages/dplyr/vignettes/dplyr.html).
It's equivalent to this SQL:

```
SELECT * FROM flights
WHERE month=1 AND day=1;
```


### base R

Base R lets us build a logical vector that we can then use to filter the
rows. We can build the vector in a few different ways.

```{R}
library(nycflights13)

flights_df = as.data.frame(flights)

month_var = "month"
day_var = "day"

# standard evaluation:
condition = flights_df[, month_var] == 1 & flights_df[, day_var] == 1

# NSE in `$`
condition = flights_df$month == 1 & flights_df$day == 1

# NSE using `with` to scope inside the data frame
condition = with(flights_df, month == 1 & day == 1)
```

Once we have the logical vector for the filter we can use it directly, or
we can use nonstandard evaluation in subset.

```{R}
# standard evaluation
f11 = flights_df[condition, ]

# NSE includes column names in scope
f11 = subset(flights_df, month == 1 & day == 1)

f11 = subset(flights_df, cond)

```


## data.table

data.table resembles base R for this task. It uses standard evaluation in
the special case when there is a single symbol in the first argument.

```{R}
library(data.table)
flights_dt = data.table(flights)

# standard evaluation
f11 = flights_dt[condition, ]

# NSE includes column names in scope
f11 = flights_dt[month == 1 & day == 1, ]
```

## dplyr

dplyr provides the largest number of ways to construct this query.  

```{R}
library(dplyr)
flights_tbl = flights

# standard evaluation
f11 = filter(flights_tbl, condition)

# NSE includes column names in scope
f11 = filter(flights_tbl, month == 1 & day == 1)

# NSE includes column names in scope and using `&` on args
f11 = filter(flights_tbl, month == 1, day == 1)

# NSE explicitly scoping inside flights_tbl
f11 = filter(flights_tbl, .data$month == 1, .data$day == 1)
```

## Computing on the language

It is possible to directly construct the code that uses NSE given the
variable names by manipulating language objects. This seems like a
complicated, indirect way of accomplishing the desired goal. Here it is for
those who are curious:

```{R}
call = substitute(flights_dt[col1 == 1 & col2 == 1, ]
    , list(col1 = as.symbol(month_var), col2 = as.symbol(day_var)))

f11 = eval(call)    # When eval() appears, think DANGER!
```

The [rlang package](https://cran.r-project.org/package=rlang) brings in a
whole framework of [tidy
evaluation](http://dplyr.tidyverse.org/articles/programming.html). I don't
have enough experience with it to comment on how well it works.


```{R}
library(rlang)

# tidyeval framework with quoting
# https://stackoverflow.com/questions/24569154/use-variable-names-in-functions-of-dplyr
month_quo = quo(month)
day_quo = quo(day)
f11 = filter(flights_tbl, (!!month_quo) == 1, (!!day_quo) == 1)

# tidyeval framework with a string
month_quo = new_quosure(as.symbol(month_var))
day_quo = new_quosure(as.symbol(day_var))
f11 = filter(flights_tbl, (!!month_quo) == 1, (!!day_quo) == 1)
```

## Thoughts


The basic queries using NSE to refer to column names in a data frame are
the easiest to analyze, because all the logic lives in just one call. 
Assuming we know these are column names.
If we compute the logical subset condition ahead of time then we need to
look around other parts of the code to see how a variable was defined.

In general data.table's approach is to use special symbols, while dplyr
uses special functions. I'm not sure if one has an advantage for code
analysis.

On a broader note, if we restrict ourselves to the class of operations on
tables that all three of these approaches to well and easily then it may be
possible to convert them to and from a common intermediate representation
that captures the desired semantics. With the right representation we might
be able to even go beyond the R language into say [Python
pandas](https://pandas.pydata.org/) and SQL. dplyr already does this in
some sense by generating SQL directly.

I think I need to understand more of the theory of databases to know if
this is feasible or not. Maybe
[rquery](https://winvector.github.io/rquery/) offers some path forward in
building abstract queries from R that we can optimize.




Here are the versions of the software used here:

```{R}
> sessionInfo()
R version 3.4.3 (2017-11-30)
Platform: x86_64-pc-linux-gnu (64-bit)
Running under: Ubuntu 16.04.3 LTS
...
other attached packages:
[1] bindrcpp_0.2       rlang_0.1.2        dplyr_0.7.2       data.table_1.10.0
[5] nycflights13_0.2.2
```
