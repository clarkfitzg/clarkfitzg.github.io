---
layout: post
title: representing semantics for data analysis code
date: 2018-02-27 13:21
comments: false
categories: R, python, metaprogramming, dplyr, data.table, semantics, database
---

This is a follow up post to [selecting rows using different R packages]({{
site.baseurl }}{% post_url
2018-02-23-selecting-rows-using-different-R-packages %}).

When analyzing data I often want to do operations that are simple in R or
Python. If the data doesn't fit into memory I write a bunch of [specialized
code]({{ site.baseurl }}{% post_url 2017-10-31-3-billion-rows-with-R %}) to
handle the size. But the semantics haven't changed; they're still simple.
It would be nice to have a system that could generate code on larger data
sets given some semantic specification. SQL does this, but I want more
functionality and extensibility than SQL provides. 

## Language independent semantics

The following code performs the same semantic operation:

```{R}
subset(flights, month == 1 & day == 1)      # Base R
flights[month == 1 & day == 1, ]            # data.table
filter(flights, month == 1 & day == 1)      # dplyr
```

How can we represent these semantics independently of the syntax?
Indeed, this code is equivalent to a simple SQL query, and if the rows are unique the
it's equivalent to [selection in relational
algebra](https://en.wikipedia.org/wiki/Selection_(relational_algebra)).

Can we capture the semantics of the query into an intermediate data
structure that's even modular to the language? That would be super cool, because
we could optimize that object directly. We could translate it to and from
any language we like. Other approaches such as [Ibis]() and [dask]() in Python and
[rquery](https://winvector.github.io/rquery/) in R do some similar things,
but they're tied to one language, so we lose the generality.

[Python's altair](https://github.com/altair-viz/altair) implements plotting
based on the [Vega
specification](https://vega.github.io/vega/examples/bar-chart/).  I'm
thinking about a similar specification for queries on tabular data, or steps in
data analysis and transformation more generally.
Facebook has something like this with
[GraphQL](http://graphql.org/learn/thinking-in-graphs/). It focuses on
graphs rather than tables.

It's also similar to intermediate representation (IR) in LLVM. We can generate
IR from several different languages. Once we have the IR we can optimize it
and run it on different architectures.

## Example

What might it look like? It should be as close to SQL as possible for a few
reasons:

- SQL is easy to read
- many people are familiar with SQL
- it will simplify translation to and from SQL

Basically I'm thinking of it as machine readable SQL, or SQL that
takes no effort to parse. Here's a rough stab at what the
query from the beginning of the post might look like:

```
{"query": {
    "SELECT": ["*"],
    "FROM": "flights",
    "WHERE": [
        ["=", "month", 1],
        ["=", "day", 1]
    ]
}}
```

We want to be able to extend it, for example by applying a user defined R
function (UDF) to one of the columns:

```
{"query": {
    "SELECT": ["month", 
        {"UDF": {"language": "R",
                "code": "function(x) x + 2L",
                "output_type": "INT",
                "properties": ["vector_func", "scalar_func"],
                "column_name": "day",
                "AS": "day_plus_two"
                },
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
                "output_type": "INT",
                "properties": ["scalar_func"],
                "column_name": "day",
                "AS": "day_plus_two"
                }}
```

Then any DSL or data analysis API like data.table, dplyr, pandas, or SQL
could potentially convert from DSL ->
query specification -> DSL for some specified set of common operations.
This allows some level of interoperability between any of them.
In
general every system will offer its own capabilities beyond the common set.


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

Then we can take the query specification and the data specification and
execute it with any code we like- R, Python, Julia, SQL, whatever. Who
cares what the underlying technology is, as long as it's fast and correct.

## Thoughts

I haven't thought much about how the specification should look, but I did
want to throw something out there to start a conversation.  This sort of
high level semantic specification would allow us to generalize beyond what
we can do by [combining R and Hive]({{ site.baseurl }}{% post_url
2017-10-31-3-billion-rows-with-R %}).  The goal is to make something
modular that goes beyond particular languages and focuses instead on the
common set of semantics for data analysis.
