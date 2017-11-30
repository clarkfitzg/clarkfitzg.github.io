---
layout: post
title: count columns in a big text file
date: 2017-11-30 14:41
comments: false
categories: bash, shell
---

Today I wanted to know how many columns were in a large compressed CSV file. Here's
a hideous way to find out:

```{sh}
$ zcat bigfile.txt.gz | head -n 1 | grep -o "," | wc -l | xargs printf "%d + 1\n" | bc -l
```

I call this hideous because it's totally unintelligble. But each element
isn't so bad:

- `zcat bigfile.txt.gz` concatenates a compressed file to `stdout`
- `head -n 1` grabs the first line
- `grep -o ","` finds the commas and prints them on new lines
- `wc -l` counts the lines
- `xargs printf "%d + 1\n"` creates the string `(ncols) + 1` since we need to add
  one to the number of commas to count the columns.
- `bc -l` uses the bash calculator to evaluate `(ncols) + 1`
