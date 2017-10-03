---
layout: post
title: column selection at read
date: 2017-10-03 14:36
comments: false
categories: R, ETL, data.table
---

__Summary__ R's `data.table` package can efficiently select columns when
reading flat text files. For this data set it's about 3 times faster than
piping the bash `cut` command into R and reading with `scan()`.

## Data

Consider the `CargoDescriptions2015.csv` data set. This is a 5.3 GB file
with 5 columns describing goods which arrived in the United States via shipping
containers in 2015.  

### data.table

Suppose we want to count the number of unique
containers. The naive way is to read in the entire data set. Using the high
performance multi-threaded `fread` function from `data.table`.

```{R, eval = FALSE}

system.time(cargo <- data.table::fread("~/data/CargoDescriptions2015.csv"))

```

This takes 2 minutes, 35 seconds on a 2016 Macbook Pro with 8 cores and
uses 5.5 GB of memory in the R process.

Since we're already using `data.table` lets use that to answer the original
question.

```{R}

system.time(num_container <- uniqueN(cargo[, "container_number"]))

nrow(cargo) / num_container

```

This takes between 9 and 10 seconds. We see that on average each container
appears about 5 times.

Can we do this faster with `data.table` by reading in only a subset of the
columns? To realistically time this we first need to remove this file from
the file cache.

```

$ vmtouch -ve ~/data/CargoDescriptions2015.csv

Evicting CargoDescriptions2015.csv

           Files: 1
     Directories: 0
   Evicted Pages: 1383045 (5G)
         Elapsed: 0.24117 seconds
```

Now lets see how long `data.table` takes to read just the columns that we
need.

```{R}

system.time(containers <- data.table::fread("~/data/CargoDescriptions2015.csv"
                    , select = "container_number", nThread = 4L))

#   Mon Sep 25 09:56:55 PDT 2017
#
#   user  system elapsed
#   107.664   5.942  32.428
#   user  system elapsed
#   110.753   6.008  33.163

system.time(num_container <- uniqueN(containers))

```

Selecting the column at the data load step reduces the load time from 2.5
minutes to about 32 seconds. This brings the total program run time from
165 seconds to around 40 seconds.

Subsequent timings of this read in the same R session are much faster, even
after forcing the file out of cache. I believe the reason for this is
because on subsequent reads all the unique strings have already been stored
in R's internal string / integer table. This would be simple enough to
verify experimentally.

The moral of the story is that the exact same calculations
can be computed more efficiently if we know ahead of time what is necessary.


### disk speed

Side note: this requires a full scan of a file that's around 5 GB. It
happened in 33 seconds. The file was not cached in memory. This means my
laptop SSD is able to load data into memory with a rate of at least 5 GB /
33 seconds = 150 MB / second. This sounds reasonable, but can I verify?

Mon Sep 25 10:06:12 PDT 2017

```

$ vmtouch -ve ~/data/CargoDescriptions2015.csv
Evicting /Users/clark/data/CargoDescriptions2015.csv

           Files: 1
     Directories: 0
   Evicted Pages: 1383045 (5G)
         Elapsed: 0.38839 seconds

$ vmtouch -t ~/data/CargoDescriptions2015.csv
           Files: 1
     Directories: 0
   Touched Pages: 1383045 (5G)
         Elapsed: 7.9652 seconds
```

Just came back to this and found that vmtouch can load this file into
cached memory in 8 seconds, implying a rate of 625 MB / second. 


### base R

For comparison, let's measure the same operation in base R. We can select
the columns we need through the `colClasses` parameter to `read.table`.

```{R}

# 607 seconds
system.time(cargo <- read.table("~/data/CargoDescriptions2015.csv"
    , header = TRUE, sep = ",", quote = "\"", comment.char = ""
    , colClasses = c("numeric", "character", "integer", "integer", "character")
    ))

# 493 seconds
system.time(containers <- read.table("~/data/CargoDescriptions2015.csv"
    , header = TRUE, sep = ",", quote = "\"", comment.char = ""
    , colClasses = c("NULL", "character", "NULL", "NULL", "NULL")
    ))

# 2.96 seconds. 3X faster in base R than data.table.
system.time(num_container <- length(unique(containers[, 1])))

```

These read times suggest that perhaps it would be desirable to just transform
regular R code into `data.table` or `iotools` if IO is the bottleneck.


### with shell preprocessing

Another way to potentially make R faster is to use the shell to select the
column of interest.
This approach is less robust than the others because it is unlikely to
handle corner cases well, ie. escape characters and quoted strings
containing the delimiter character.

Running on the above data set I see issues with 
value `"SACRAMENTO,"`, which gets incorrectly cut to
`"SACRAMENTO`.

I'm expecting 43754131 observations.

```{R}

system.time(containers <- read.table(
    pipe("cut -d , -f 2 ~/data/CargoDescriptions2015.csv")
    , header = TRUE, sep = ",", quote = "\"", comment.char = ""
    , colClasses = "character"
))

# Didn't work:
#
#Warning message:
#In scan(file = file, what = what, sep = sep, quote = quote, dec = dec,  :
#  EOF within quoted string
#  > dim(containers)
#  [1] 8294588       1
#

system.time(containers2 <- scan(
    pipe("cut -d , -f 2 ~/data/CargoDescriptions2015.csv")
    , what = character(), skip = 1, sep = "\n"
))
# Read 43754131 items
#    user  system elapsed
#    147.888   2.216  97.881

length(containers2)

```

The second command seems to work, with the caveats above. This takes base R down
from 493 seconds to 98 seconds, a factor of 5. It also should use much less
memory because R only ever sees the column that it needs. `data.table` is still 
3 times faster than this and much more robust.

If I'm going to do something like this automatically I need to be able to
create these `cut` commands. It would be better to rely on as few external
dependencies as possible, bash `cut` is not available on Windows. What if I
used Python?  That's another external dependency. It wouldn't surprise me
if it was as fast here as the cut command. Now I'm curious.

```{R}

system.time(containers2 <- scan(
    pipe("python ~/data/select_column.py ~/data/CargoDescriptions2015.csv 2")
    , what = character(), skip = 1, sep = "\n"
))
# Read 43754131 items
#    user  system elapsed
#    188.837   2.993 138.850

```

Of course introducing a dependency on another programming language is far
from ideal. I wonder if there's a way to pipe the R commands to get
pipeline parallelism?  Judging by the user and elapsed times here we did
get some pipeline parallelism, both for the Bash and Python approaches.

What is the limiting factor here? Preprocessing or other?
I can find best case performance by creating another file with only the
column of interest and then reading that.

```{R}

N = 43754131 

system.time(containers2 <- scan("~/data/container_number.csv"
    , what = character(), skip = 1, sep = "\n", n = N
))

# Read 43754131 items
#    user  system elapsed
#     70.371   0.517  70.899


# scan() seems to have three parameters similar to `n`
system.time(containers2 <- scan("~/data/container_number.csv"
    , what = character(), skip = 1, sep = "\n", n = N, nlines = N
))
# Read 43754131 items
#    user  system elapsed
#     70.721   0.537  71.273


```

The times above are consistent even when I remove the file from cache. This
makes sense based on what I saw above with `data.table`. Then around 70
seconds is a lower bound for how fast this load can happen with `scan`. The
Python and bash `cut` versions are 2 to 3 times slower than this.
