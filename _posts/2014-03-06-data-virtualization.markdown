---
layout: post
title: "data virtualization"
date: 2014-03-06 07:01:43 -0800
comments: true
categories: data virtualization enterprise
---

Yesterday at work I heard an excellent presentation on [data virtualization](http://en.wikipedia.org/wiki/Data_virtualization). The data infrastructure in a large enterprise environment can be very complex. Data virtualization helps by abstracting logical models from the physical models, leading to a layered approach to data reminiscent of the [7 layer network model](http://en.wikipedia.org/wiki/OSI_model). SQL is the common glue that joins all the layers together.

The idea is Extract, Transform, Load (ETL) jobs are expensive, since they involve moving lots of data across the network and syncing data in many different locations. With data virtualization you create views rather than physical tables. The views consist of logical joins and queries. A single view could be pulling data from many different physical tables. For example, a single view could be pulling data from Hadoop, a REST web API, a delimited file on a file server, and from an Oracle database. To the end user this appears to be a single table in the virtualization layer, and it saves them the trouble of integrating all the data in their client application every time someone needs a similar view. So the main advantages are development speed and flexibility.

The downside to data virtualization is that it's limited by the size of data it can handle. A million row join is expensive no matter where you do it. Hence the data virtualization layer can become the bottleneck. Another issue is latency; responses won't be as fast as a performant database, since there are more layers in between. A third issue is where the transformational logic sits. If the logic that transforms the raw data into useful business measures is totally contained in the data virtualization layer then you must go through this layer or else replicate the logic in other places. This can create headaches down the road.

In summary, data virtualization offers great potential for simplifying ETL's and the enterprise data environment. It will become more important in the future as data sources proliferate. But it's not a perfect solution.
