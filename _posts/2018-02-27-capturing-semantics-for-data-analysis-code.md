---
layout: post
title: capturing semantics for data analysis code
date: 2018-02-27 13:21
comments: false
categories: R, python, metaprogramming, dplyr, data.table, semantics
---

This is a follow up post to [selecting rows using different R packages]({{
site.baseurl }}{% post_url
2018-02-23-selecting-rows-using-different-R-packages %}).

## Language independent semantics

The following code performs the same semantic operation:

```{R}
subset(flights, month == 1 & day == 1)      # Base R
flights[month == 1 & day == 1, ]            # data.table
filter(flights, month == 1 & day == 1)      # dplyr
```

Because the semantics are the same it should be possible to represent these
semantics in a way that's independent of the syntax. Indeed, this code is a
simple SQL query, and if the rows are unique the it's equivalent to
[selection in relational
algebra](https://en.wikipedia.org/wiki/Selection_(relational_algebra)).

The more we know about the semantics of the desired operation the more we
can use this knowledge to evaluate the code in a different way. 

Can we capture the semantics of the query into an intermediate data
structure that's modular to the language? That would be super cool, because
we could optimize that object directly. We could translate it to and from
any language we like. Other approaches such as [Ibis]() and [dask]() in Python and
[rquery](https://winvector.github.io/rquery/) in R do some similar things,
but they're tied to one language, so we lose the generality.

This is really exciting to me.

Jake Vanderplas did something similar with [plotting in Python's
altair](https://github.com/altair-viz/altair) that implements plotting
based on the [Vega
specification](https://vega.github.io/vega/examples/bar-chart/).
I'm thinking about a similar specification queries on tabular data, or
steps in data analysis and transformation more generally.

It's also similar to intermediate representation (IR) in LLVM. We can generate
IR from several different languages, and then optimize it and run it on
different architectures.


## Example

What might it look like? It should be as close to SQL as possible for a few
reasons:

- SQL is easy to read
- many people are familiar with SQL
- it will simplify translation to and from SQL

Basically I'm thinking of it as machine readable SQL, or SQL that
takes no effort to parse. Here's a rough stab at the specificiation for the
query in the beginning of the post.

```
{"query": {
    "SELECT": "*",
    "FROM": "flights",
    "WHERE": [
        ["=", "month", 1],
        ["=", "day", 1]
    ]
}}
```

We want to be able to extend it, for example apply a user defined R
function (UDF) to one of the columns:

```
{"query": {
    "SELECT": ["month", 
        {"UDF": {"language": "R",
                "code": "function(x) x + 2",
                "column_input": true,
                "column_name": "day"},
        "AS": "day_plus_two"
        }
    ],
    "FROM": "flights"
}}
```

Suppose the user only has access to base Python, not R. Then the UDF might
look something like this:

```
        {"UDF": {"language": "Python",
                "code": "lambda(x) x + 2",
                "column_input": false,
                "column_name": "day"}
```

A domain specific language should be able to convert from DSL ->
intermediate form -> DSL for some specified set of common operations. In
general every system will offer its own capabilities beyond these.


## Data

We can represent metadata along with the data in a similar way. We can
build a data description that allows us to generate code that doesn't
require any inference. Granted, many packages do a great job at inference,
but we can generate more specific code and remove assumptions along with
whole classes of errors and inconsistency if we don't have to do this
inference.

WHOA- crazy idea. We could generate and use compiled code. Not sure this
would be any faster than fast approaches in R's `iotools` or `data.table` though.

Suppose flights is a table in a text file. Here's what the metadata might
look like:

```
{"table": {
    "path": "flights.csv",
    "text": true,
    "delimiter": ",",
    "header": false,
    "column_names": ["day", "month", "a", "b", "c"],
    "column_types": ["INT", "INT", "VARCHAR(200)", "FLOAT", "BOOLEAN"],
    "rows": 10000
}}
```

Facebook has something like this with
[GraphQL](http://graphql.org/learn/thinking-in-graphs/). It focuses on
graphs rather than tables.
