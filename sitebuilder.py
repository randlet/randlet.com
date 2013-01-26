import collections
import os
import sys

from flask import Flask, render_template, abort, url_for
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)


valid_projects = collections.OrderedDict()
valid_projects["qatrack"] = {
    "symbol":"Qa",
    "title": "QATrack+",
    "subtitle":"A Radiotherapy QA Tool",
    "description": "QATrack+ is an open source tool written in Python for recording and monitoring the quality control program of a radiotherapy clinic",        
    "links":[
        {
            "icon":"icon-play",
            "href":"/qatrackplus/",
            "text":"Live Demo",
            "title":"Try a live demo of QATrack+",
        },        
        {
            "icon":"icon-edit",
            "href":"http://bitbucket.com/tohccmedphys/qatrackplus/",
            "text":"Source",
            "title":"Download the source code",
        },
    ],    
}

valid_projects["orbis"] =  {
    "symbol":"Or",
    "title": "Orbis",
    "subtitle":"Simple Huckel Molecular Orbital Calculations",
    "description": "Orbis is a free and open source program for performing simple Huckel molecular orbital calculations.",        
    "links":[
        {
            "icon":"icon-download",
            "href":"/static/downloads/install_orbis.exe",
            "text":"Installer",
            "title":"Download a Windows installer",
        },        
        {
            "icon":"icon-github",
            "href":"http://github.com/randlet/orbis/",
            "text":"Source",
            "title":"Download the source code",
        },
    ],
}
    
valid_projects["randlet.com"] = {
    "symbol":"Ra",
    "title": "randlet.com",
    "subtitle":"Personal Homepage written with Flask/Frozen Flask",
    "description": "Source code for the webpage you're currently visiting :)",        
    "links":[
        {
            "icon":"icon-edit",
            "href":"https://bitbucket.org/randlet/randlet.com/",
            "text":"Source",
            "title":"Download the source code",
        },
    ],    
}



@app.context_processor
def inject_tags():
    tags = []
    for p in pages:
        tags.extend(p.meta.get('tags',[]))
    tags = [x[0] for x in collections.Counter(tags).most_common(10)]
    return {"tags":tags}

@app.route('/')
def index():
    context = {
        "page_title":"Programming, Science &amp; Life",
        "pages":pages,
    }
    return render_template('index.html',**context)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)

@app.route('/projects/')
def projects():
    return render_template('projects/index.html', projects=valid_projects)

@app.route('/projects/<path:project>/')
def project(project):
    
    if project not in valid_projects:
        abort(404)
    return render_template("projects/%s/index.html"%project,project=valid_projects[project],project_id=project)

@app.route('/projects/<path:project>/<path:subpage>/')
def project_subpage(project,subpage):    
    return render_template("projects/%s/%s.html"%(project,subpage),project=valid_projects[project])
        
@app.route('/blog/')
def blog():
    return render_template('blog.html', pages=pages)

@app.route('/blog/<path:path>/')
def posts(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

@app.route('/papers-talks/')
def papers_talks():    
    return render_template("papers_talks.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

    
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)