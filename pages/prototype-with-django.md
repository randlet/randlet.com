title: Prototyping Interfaces with Django (CBV version)
date: 2013-03-15
tags: [general, python, django, cbv, templates]
blurb: A CBV update to Dave Bertrand's "Better UI Prototyping with a Django Twist" post
thumbnail: template.jpg
attribution: http://www.flickr.com/photos/robglinka/6041889401/

Dave Bertrand over on the Imaginary Landscape blog had a <a
href="http://www.chicagodjango.com/blog/better-ui-prototyping-django-twist/"
title="Imaginary Landscape Blog Post on UI Prototyping with Django"> nice
tip</a> on a convenient way to do UI prototyping with Django templates. I
like this approach since, as Dave points out, you can take full advantage of
the Django template language (template tags, control structures etc) and it
means when you're done prototyping you are left with usable Django
templates rather than plain HTML files.

Dave's post uses `django.views.generic.simple.direct_to_template` which has
been <a href="https://docs.djangoproject.com/en/1.5/internals/deprecation/#id2" title="Django 1.5 depracation plans">deprecated in Django 1.5</a>. It's easy enough to modify his solution to use
a TemplateView instead of the `direct_to_template` generic view. Just create
a little MockUp class in your urls.py file like the following:

    :::python 

    from django.conf.urls import patterns, include, url
    from django.views.generic import TemplateView
        
    class MockUp(TemplateView):
        def get_context_data(self,**kwargs):
            self.template_name = self.kwargs["template_name"]
            return super(MockUp,self).get_context_data(**kwargs)
    
    
    urlpatterns = patterns('',
        url(r'^(?P<template_name>.*)$', MockUp.as_view()),    
    )
    
You can now run the dev server and visit 127.0.0.1/foo.html and have your
django template foo.html rendered.

It's not quite as slick as the `direct_to_template` version but it does give
you the opportunity to stick a couple other things in the template context if
needed.
