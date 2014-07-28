---
layout: post
title: python mock objects
date: 2014-07-15 06:58
comments: false
categories: python, testing, software development
---

The more I write tests, the more I enjoy it. Some more experienced programmers turned me on to test driven development, and I think it's the way to go if you want to write robust software. Writing the test first has really changed how I think about the programming task. It forces me to think about the API's that I'm creating, and the logic behind the layers of abstraction within a program.

The goal in writing unit tests is to write a test for each specific, isolated piece of functionality. That means that the dependencies like databases and networks should be mocked, rather than called. All you care about for a unit test is that the code is doing the correct thing, not whether that external system is up and responding appropriately.

Here's an example unit test to demonstrate.

```
@mock.patch('webstuff.requests.get')
def test_download(mock_get):
    response = webstuff.download('example')
    url = 'http://www.example.com'
    mock_get.assert_called_with(url)
```

The `patch` decorator is applied to `requests.get` within `webstuff`, the module which is being tested. The test function definition takes an argument which becomes the mock object. Now instead of actually doing the download, this code just makes sure that `webstuff` built and called the correct URL.
