---
layout: post
title: base memory usage of data analysis processes
date: 2014-10-12 08:03
comments: false
categories: R, Python, Memory
---

I've been taking a linear regression class, and have seen lots of formulas
regarding the least squares regression estimate with one variable. What's a
good application for these formulas? 

One use case is in remote sensing.
Suppose that you have a sensor that's generating a stream of numbers with
respect to time. Single variate regression can be used to estimate the rate
of change of those numbers in real time. In this application we might
expect the sensor to have little computational power- maybe it's just
an [Arduino board](http://www.arduino.cc/) or a Rasberry Pi. Then it makes sense to have a
linear regression process with as little memory overhead and as few
software dependencies as possible.

This is an appealing idea because we're putting more intelligence into
distributed components of a system. If all the 100 sensors can
automatically do their own data analysis then there's less work for a central
monitoring process to do. 

So then I wondered, what's the minimum amount of computer resources that
are needed to do anything at all in languages common for data analysis?

Here is a simple test with Numpy.

```
'''
How much memory will this take up in Numpy?
'''

import time

#import numpy as np
from numpy.random import randn

#a = np.random.randn(100)
a = randn(100)

time.sleep(10)
```

Running this and looking at the activity monitor on a Macbook I observe
that it uses 13.6 MB of memory in Python 3.4. Uncommenting the lines to import the whole
Numpy library uses 13.9 MB. We can do the same thing in R:

```
a = runif(100)

Sys.sleep(10)
```

The R script shows 20.6 MB of memory on the activity monitor. If we do it
in pure Python (without Numpy):

```
import time

a = list(range(100))

time.sleep(10)
```

This takes 3.6 MB of memory.

## Conclusion

The R and the Numpy version are on the same order of magnitude, but the
pure Python version is much smaller. The appealing part here is that a pure Python
is a much lighter dependency than either R or Numpy, which means it will be
simpler to put on a small board or a micro Linux system (since Linux
distros include Python). 
