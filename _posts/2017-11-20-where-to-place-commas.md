---
layout: post
title: where to place commas
date: 2017-11-20 08:43
comments: false
categories: style, programming, SQL
---

I prefer to write code in a way that visually exposes syntax errors.
Furthermore, I like to be able to easily extend the code by copying and
pasting lines. This is easier if all the lines look the same, and place the
necessary syntactic tokens, ie. commas, in a consistent place.

### Example 1

Can you glance at this code and immediately identify the two syntax errors?

```{sql}
CREATE TABLE fundamental_diagram (
    station INT,
    n_total INT,
    n_middle INT,
    n_high INT,
    left_slope DOUBLE
    left_slope_se DOUBLE,
    mid_intercept DOUBLE,
    mid_intercept_se DOUBLE,
    mid_slope DOUBLE,
    mid_slope_se DOUBLE,
    right_slope DOUBLE,
    right_slope_se DOUBLE,
);
```

I need to look carefully to determine that `left_slope DOUBLE` does not
have a trailing comma. The last line is also wrong, because it has a
trailing comma.

### Example 2

Here's another example of the same code with the same type of syntax error:

```{sql}
CREATE TABLE fundamental_diagram (station INT 
    , n_total INT 
    , n_middle INT 
    , n_high INT 
    , left_slope DOUBLE
    , left_slope_se DOUBLE
    , mid_intercept DOUBLE
    , mid_intercept_se DOUBLE
    , mid_slope DOUBLE
    mid_slope_se DOUBLE
    , right_slope DOUBLE
    , right_slope_se DOUBLE
);
```

I can quickly spot the missing comma in front of `mid_slope_se DOUBLE`
because all the commas are anchored in a visually prominent place.

### Conclusion

Style is only useful to the extent that it helps us write code that's
correct and easy to read.  Some might say the leading commas make the
second example "ugly". The second way is as easy to read as the first
example, and it's easier to spot errors.
