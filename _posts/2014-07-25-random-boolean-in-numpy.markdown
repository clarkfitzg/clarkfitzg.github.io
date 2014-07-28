---
layout: post
title: random boolean in numpy
date: 2014-07-25 21:50
comments: false
categories: Numpy, Python
---

I was curious how Numpy stores booleans, so I decided to explore it a bit. Right at the top of the [Numpy docs](http://docs.scipy.org/doc/numpy/user/basics.types.html) it says that the boolean type is stored as a byte. That's 8 bits instead of 1, but it probably makes computation more efficient.

Here's the experiment:

```
In [2]: tf = np.array([True, False])

In [3]: tf
Out[3]: array([ True, False], dtype=bool)

In [4]: a = np.random.choice(tf, int(1e7)) 
```

`tf` is a Numpy array containing `True` and `False`. `np.random.choice` samples 10 million times in this case. The system monitor verified that this line of code resulted in a data structure occupying 10 MB in memory.

## Interesting Zeros

Consider this little line of code:

```
In [10]: b = np.zeros(int(1e7))

In [11]: b.dtype
Out[11]: dtype('float64')
```

One might expect it to create 10 million floating point numbers, resulting in an additional memory use of 8 bytes * 10 million ~ 80 MB of memory. This is what happens for `np.ones`. But `np.zeros` uses almost no memory. This means that something very clever is happening, and it's using a sparse data structure. 

It's the subtleties that make these things interesting.
