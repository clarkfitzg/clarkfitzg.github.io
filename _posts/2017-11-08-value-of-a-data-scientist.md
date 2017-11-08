---
layout: post
title: value of a data scientist
date: 2017-11-08 11:13
comments: false
categories: philosophical, data science, career
---

> What's the difference between a data analyst and a data scientist?
> Initiative, independence, and inquisitiveness.

- Duncan Temple Lang, director of the UC Davis Data Science Initiative

This statement made me think about what it means to be a data scientist.  I
often feel sheepish when telling people that's what I do, even though I'm
in a statistics PhD program and I've been analyzing data daily since 2012.
I agree with Duncan's definition, but would like to expand on it a bit and
characterize data scientists in business by what they can do:

Given any kind of data set, they can find some meaningful
insights in it. For example, given data in obscure `ADT` format they can find
software to load it into their preferred analysis environment, make plots,
and discover that missing values are represented by `-1`.

They can help transition the results of an informal analysis into a more
robust engineering solution. For example, they discover that a linear model
works well for a prediction task, and then explain what the linear model
does and help translate it into Clojure, a language they're unfamiliar
with, for use by the engineering team. This example highlights a second
skill, the ability to quickly pick up and use new technologies.

They are familiar with and sufficiently skeptical of statistical and
machine learning techniques. For example, when analyzing a time series data
they can understand the assumptions and model of ARIMA. They're not
necessarily experts in time series, but they know where to look and can
grasp the key ideas well enough to quickly produce valid results.

They can present results to a non technical audience in a way that makes
sense. For example, they might show how a thoughtfully designed experiment
will show a causal relationship, thus supporting business decisions.
