---
layout: post
title: so many blog platforms
date: 2014-07-14 20:05
comments: false
categories: 
---

I've decided to start blogging more regularly.

This seemed like a good time to switch platforms. I was on Github pages before, and that was ok. I just didn't care for all the front end web business. All I want to do is write my posts in markdown with Vim and Git. That's all I ask. It was nearly impossible to find a blog post or tutorial that laid out the steps for doing that.

So I hunted for a more conventional blogging platform with a GUI. [Medium](https://medium.com/) was quite nice with its minimal UI, but then I tried to write a block of code. No dice. It only does single lines of code. Not inline code, and not multiple line blocks. That doesn't work for me. [Svtble](https://svbtle.com/) looked good, since it supports [markdown](http://daringfireball.net/projects/markdown/), but they're not accepting new bloggers at the moment. That puts them out.

Earlier I had tried Wordpress, but didn't care for the complexity. I tried [tumblr](https://www.tumblr.com/), but managed to mix up my password in Lastpass by generating three different passwords. Happens sometimes. They didn't have a recover password link, so I moved on.

I found myself back at [Jekyll](http://jekyllrb.com/) and Github Pages. This time I looked into it in a little more detail to figure out that it can create minimal pages with minimal effort. From the command line:

```
$ jekyll new blogname
```

Push the repo to an appropriately named Github repo and you've got a blog. This was nice for me because the file structure was immediately obvious. When I did it earlier I thought that my blog was forking Jekyll itself. But Jekyll just generates the static site.

In the end, it's nice to have all my posts together in the markdown source, and version controlled with Git. I came full circle and went back to Github pages.
