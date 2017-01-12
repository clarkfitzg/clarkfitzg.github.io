---
layout: post
title: example statistical computation on GPU
date: 2017-01-12 10:48
comments: false
categories: GPU, math, Julia, C
---

{% include math.html %}

## Summary

It's possible to speed up heavy numerical computation by an order of magnitude by
writing OpenCL kernels and running them on a GPU (graphical processing
unit).

## Motivation

The original motivation for this calculation was to approximate the
log likelihood $$L(\theta)$$ for an n dimensional multivariate normal $$X \sim N(0, \Sigma)$$
where $$\Sigma = g(\theta)$$ for $$p$$ dimensional $$\theta$$ with $$p << n$$.
We're not assuming any kind of special structure for $$\Sigma$$ beyond this. More
concretely, for data on the cosmic microwave background from the Planck
telescope we might have $$n = 10^7$$ and $$p = 6$$.
Computing the exact likelihood requires a Cholesky decomposition which is
$$O(n^3)$$, which is prohibitively expensive in this case.

If these likelihood approximations are fast enough then we can use more
efficient numerical optimization methods that may require many function
evaluations.  Then we end up with faster and more accurate methods to find
the maximum likelihood estimators for $$\theta$$. 

## Computation

The general idea is to use Vecchia's approximation together with [thin
plate
splines](https://en.wikipedia.org/wiki/Thin_plate_spline#Radial_basis_function)
to quickly approximate the likelihood. Every coordinate of $$X$$ contributes
to the likelihood, so we represent that contribution with a thin plate
spline. Mathematically, following the notation from Wikipedia:

$$
    L(\theta) \approx \sum_{i = 1}^n \sum_{j = 1}^k c_{ij} \phi(\Vert \theta - w_{ij} \Vert)
$$

where $$\phi(x) = x^2 \log x$$ is the mathematical kernel, not to be confused
with the OpenCL kernel. $$c_{ij}, w_{ij}$$ are the spline coefficients and
control points, respectively. We haven't yet considered how to estimate
these, but it will definitely have to be done in order to apply this method.

Rather than performing the outer sum we computed a vector of length $$n$$
containing the spline evaluations. In psuedocode:
```
out = vector(n)
for i in 1:n:
    out[i] = thin_plate_spline(x, coef[i, ], control_pts[i, ])
```
The body of this loop is the OpenCL compute kernel.

## Timings

We wrote this in R, C, and Julia and tested it with random inputs. We set
$$n = 10^7$$ and chose $$k = 10$$ so that we wouldn't run out of memory on
a Mac GPU.

Here are the timings on an nVidia GPU:

```
Transfer input to device (GPU): 0.140000 sec
Run compute kernel:             0.010000 sec
Return output to host (CPU):    0.080000 sec
Total:                          0.230000 sec

Transfer input to device (GPU): 0.130000 sec
Run compute kernel:             0.030000 sec
Return output to host (CPU):    0.060000 sec
Total:                          0.220000 sec
```


