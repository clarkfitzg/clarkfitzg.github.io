#! /usr/bin/env python
'''
post.py

Make new Jekyll blog posts
'''

import os
import subprocess
import time

title = os.sys.argv[1]
date = time.strftime('%Y-%m-%d')


top = '''---
layout: post
title: {}
date: {}
comments: false
categories: 
---

'''.format(title, time.strftime("%Y-%m-%d %H:%M"))

filename = '-'.join([date] + title.split()) + '.md'

with open(filename, 'w') as f:
    f.write(top)

subprocess.call(['vim', filename])
