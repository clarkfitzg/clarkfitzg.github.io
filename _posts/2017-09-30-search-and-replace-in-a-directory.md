---
layout: post
title: search and replace in a directory
date: 2017-09-30 09:10
comments: false
categories: bash, linux, software engineering
---

The last couple days I've been refactoring a project's codebase. I would
like to replace every instance of the string `findvar` in any file with
`find_var` to make the naming scheme more consistent. 

```{bash}

grep --files-with-matches -r "findvar" * | xargs sed -e "s/findvar/find_var/g" -i ""

```

This is not the safest, most efficient, or most elegant way to do this, but
it's the way that I'm most likely to remember.


## Other Ways

I could do this by individually opening and editing the following files:

```{bash}
$ grep -r "findvar" * | cut -f 1 -d ":" | uniq
R/apply.R
R/canon.R
R/subset.R
R/utils.R
man/findvar.Rd
tests/testthat/test_utils.R
```

As a side note, the `grep` command above can be done more efficiently,
since `grep` can stop searching a file as soon as it finds a single match.
This might be handy if you're searching very large files and relatively few
of them don't match the expression.

```{bash}
$ grep --files-with-matches -r "findvar" *
```

Now that we've found the files `sed` (streaming editor) can edit them all
simultaneously:

```{bash}
grep --files-with-matches -r "findvar" * | xargs sed -e "s/findvar/find_var/g" -i "back"
```

`xargs` takes the list of files produced by `grep` and passes them to `sed`
as the list of files.  If we instead piped the `grep` output directly to
`sed` then `sed` would perform the substitution on the file names, which
isn't what we want here.

The `-i "back"` argument makes a backup copy of each file by adding
`"back"` to each file name before modifying the files in place.  Often I
use `-i ""` to modify the files in place without backups from within a Git
repository, since Git can easily recover the files when I make a mistake.

The command above is redundant because we search for `findvar` twice.
Instead we can just process the files we're interested in, those with file
extensions `.R` and `Rmd`.  `man/findvar.Rd` is automatically generated so
I don't need to process it.

```{bash}
find -E . -regex ".*\.R(md)?" | xargs sed -e "s/findvar/find_var/g" -i ""
```

The `-E` flag says to use extended regular expressions. These are the
modern regexes that people are probably more familiar with.

It's less important that I only match `.R` and `.Rmd` files and more
important that I do not attempt to process files inside the `.git`
directory. The following command lists all the files except those in the
`.git` directory:

```{bash}
find . \! -path "./.git/*" -type f
```

This doesn't work to combine with `sed` because I end up passing `.png`
image files which contain illegal byte sequences for a regex.
