---
layout: post
title: ideas for software engineering lessons
date: 2019-07-12 09:50
comments: false
categories: software engineering, teaching
---

Some notes on what I would like to teach about software engineering.

TODO: Find real examples in real code bases that illustrate these points.


### Comments

Comments should be meaningful, and tell you something that's not obvious from the code.

Good:
```{r}
# Initial state for computing the fibonacci sequence
x[1] = 0
```

Bad:
```{r}
# Assign 0 for the first element
x[1] = 0
```


### Dependencies and software reuse

Find a balance between reusing code and having excessive dependencies.


### Commit messages

Why did you do what you did?
Did it fix something or add new functionality?
Was it just cosmetic / stylistic?


### Testing

More tests are not necessarily better.
Don't write tests that tie you to implementation details, if you can help it.
Test the things that matter.


### Names

Few would be perplexed by a function named `get_data_from_connection`.
Few would know what a function named `get_dfc` does.
When in doubt, err on the side of verbose names.
Try to keep it under 25 characters.


### Functions

Write small, easy to understand functions.
Decompose them into simpler ones, and give them explicit names.
One general technique is to look for big indented blocks in your code and make those into functions.
These could be the bodies of loops or conditional statements.


### Simplicity

Strive to write simple code, using basic data structures whenever possible and convenient.
Don't show off your knowledge of the language
