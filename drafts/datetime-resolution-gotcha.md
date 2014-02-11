title:  A Python Datetime Precision Gotcha
date: 2013-11-22
tags: [python, datetime, precision, django]
blurb:  Beware of different resolutions on Python datetime time functions.
thumbnail: time.jpg
attribution: http://www.flickr.com/photos/opendemocracy/2871333638/

I recently got a bug report from a user about some objects being pulled
from a database that were being displayed wth an unexpected order (they were
Django model instances, but that's largely irrelevant).  I was initially
pretty confused since the objects were being ordered by a `created` datetime field
that was set to the current time when the object was created. The objects
were being created in a loop that looked similar to this:

    :::python
    for data in all_data:
        now = datetime.datetime.now()
        obj = MyModel(
            foo=bar,
            ...
            created = now,
            ...
            baz=qux,
        )


and then later on I would sort things by the `created` field.

Unfortunately there is somewhat of a subtle bug lurking here


