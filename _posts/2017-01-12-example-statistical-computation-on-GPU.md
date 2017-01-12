---
layout: post
title: example statistical computation on GPU
date: 2017-01-12 10:48
comments: false
categories: GPU, math, Julia, C
---

{% include math.html %}

## Summary

It's possible to speed up heavy numerical computation by writing
[OpenCL](https://www.khronos.org/opencl/) kernels and running them on a GPU
(graphical processing unit).

__Disclaimer__ I'm a novice C programmer, and this is my first time writing
OpenCL. So there are almost certainly safer or faster ways to do things.

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
a Mac laptop GPU.

C and Julia ran at a similar speed, between __3 and 4 seconds__ on my
desktop.  Here are a couple timings on a more powerful nvidia GPU, the Tesla
K20c which has 2500 cores:

```
Transfer input to device (GPU): 0.14 sec
Run compute kernel:             0.01 sec
Return output to host (CPU):    0.08 sec
Total:                          0.23 sec

Transfer input to device (GPU): 0.13 sec
Run compute kernel:             0.03 sec
Return output to host (CPU):    0.06 sec
Total:                          0.22 sec
```

Evaluating the compute kernel takes around 0.02 seconds. If we fix all
the inputs except the small $$p$$ vector $$\theta$$ and take the extra step
of summing the output vector to evaluate the scalar valued likelihood
function then the data transfer time will be effectively 0 for any
subsequent evaluation.  Hence this method can potentially result in
function evaluations two orders of magnitude faster than CPU code. 

These faster function evaluations can potentially be very helpful for
numerical optimization routines.

## Final Thoughts

Most of my programming experience is in high level languages like Python
and R. This is really my first foray into the low level world of creating
buffers and directly transferring memory onto devices. I learned a ton, and
also learned how much I don't know.

The [OpenCL Programming
Guide](https://www.amazon.com/OpenCL-Programming-Guide-Aaftab-Munshi/dp/0321749642)
explains the basic concepts well.

Code and notes can be found here in the [fastgauss Github
repo](https://github.com/clarkfitzg/fastgauss), especially in the [tps
subdirectory](https://github.com/clarkfitzg/fastgauss/tree/master/tps).
