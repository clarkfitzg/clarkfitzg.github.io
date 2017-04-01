---
layout: post
title: pushing R into swap space
date: 2017-03-29 13:20
comments: false
categories: 
---

What happens to performance when data gets too large for memory?
Formerly there was a limit for how large a vector could be in R, but that
has been lifted. This means that we can create objects which are larger
than memory and the operating system will spill them over into swap space.

To find out I did a little experiment creating and computing
on a vector of length `n`, where `n` was chosen to take up a fixed fraction
of the system memory. I ran [this
code](https://github.com/clarkfitzg/phd_research/blob/master/proposal/swap/mean.R):

```
x <- rnorm(n)
xbar <- mean(x)
```

## Spinning Disk

Here's what happened with a conventional spinning hard disk:

![]({{ site.url }}/assets/spinning_disk_swap.png)

Timings start off almost perfectly linear in `n`, which is to be expected because the
operations are O(n). Once it starts swapping to disk it immediately
becomes more than an order of magnitude slower. Then performance 
follows a rough linear trend with quite a bit more variability.

No larger values of `n` worked because this code ran on a system with 8 GB of
memory and 8 GB swap. If you try to make something too big R refuses with
this message:

```
Error: cannot allocate vector of size 20 Gb
```


## SSD

What if we swap to an SSD (solid state drive)? 

![]({{ site.url }}/assets/ssd_swap.png)

Once swapping begins it only
becomes about 2 - 3 times slower instead of 10 - 20 times slower.
It continues to slow down once it's swapping, but the rate is only about
three times that of being wholy within memory. This is much better
performance all around than the spinning disk.

Big thanks to our excellent UC Davis systems administrator Nehad Ismail for
installing an SSD on one of our servers and configuring the swap.

## Conclusions

Performance in R hits a wall once one starts going to disk, and this is why
it's to be avoided. If you're actually using objects this big then you need
to be well under these memory limits, since objects in R generally get
copied right and left.

However, this does suggest that SSD's have much to offer when it comes to
improving performance and creative solutions. It's exciting to see such
active work in projects like [R's new fst](http://www.fstpackage.org/).
