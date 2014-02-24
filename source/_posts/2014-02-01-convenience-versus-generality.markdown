---
layout: post
title: "Convenience versus Generality"
date: 2014-02-01 12:41:35 -0800
comments: true
categories: Linux Python
---

## The Task
Store the names of files in a specific directory as a list of strings in Python. More specifically, I have three data files in a directory:
```
$ ls /Users/clark/data/funproject
alpha.csv   bravo.csv   charlie.csv
```
I would like to have the following list of strings in Python:
```
>>> names
['alpha.csv', 'bravo.csv', 'charlie.csv']
```

## The Easy Way
I was working inside [Ipython Notebook](http://ipython.org/notebook.html), so I tried doing the easiest thing possible:
```
In [1]: names = ! ls /Users/clark/data/funproject
```
Surprisingly, it worked! I proceeded with what I was doing. The path to the data was needed in another place, so I stored it as a variable called `datapath`. After a little code organization I was left with this in my script:
```
datapath = '/Users/clark/data/funproject'
names = ! ls /Users/clark/data/funproject
```
Now it was obviously poorly organized. Furthermore, this will only run with IPython. Not good.

## More General
After a visit to [Stack Overflow](http://stackoverflow.com/questions/8880461/python-subprocess-output-to-list-or-file) I ended up with this, which is better. (Thanks [@Gary](http://stackoverflow.com/users/72911/gary-van-der-merwe)
```
datapath = '/Users/clark/data/asus/'
names = subprocess.check_output(['ls', datapath]).splitlines()
```
However, it seems clunkier than it has to be, and I wouldn't expect it to work in Windows. 

## Pythonic
Man, if I had only read the full post on Stack Overflow sooner I would have seen the Pythonic way to do it, which is:
```
datapath = '/Users/clark/data/asus/'
names = os.listdir(datapath)
```
According to the [Python Documentation](http://docs.python.org/2/library/os.html#os.listdir) this should work on Windows as well. Clean. Clear. Simple.
