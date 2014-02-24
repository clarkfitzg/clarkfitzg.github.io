---
layout: post
title: "May the Source be with you"
date: 2014-02-23 19:29:23 -0800
comments: true
categories: open source, statistics, rstats
---

We're a little over halfway through the stats class offered online by [Stanford](https://class.stanford.edu/courses/HumanitiesScience/StatLearning/Winter2014/), and it's rocking my world. So, so good. It helps that I have projects at work that involve all of these concepts.

The other day I had a look at the source code for the [glmnet](http://cran.r-project.org/web/packages/glmnet/index.html) package, because I had a question on how the lambda coefficients controlling regularization for ridge regression and the Lasso were generated. I downloaded it from CRAN and poked around the file structure. It was neat to see how the R code called the Fortran, and it gives me a much better idea of how I would go to write a package.
