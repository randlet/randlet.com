import collections
import os
import sys

from flask import Flask, Response,render_template, abort, url_for
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
            "href":"/qatrack/",
            "text":"Live Demo",
            "title":"Try a live demo of QATrack+",
        },        
        {
            "icon":"icon-edit",
            "href":"http://bitbucket.org/tohccmedphys/qatrackplus/",
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


papers = collections.OrderedDict()
papers["Papers"] = [
    {
        "file":"Ta06b.pdf",
        "title":"Benchmarking BrachyDose: voxel-based EGSnrc Monte Carlo calculations of TG&mdash;43 dosimetry parameters",
        "authors":"R. E. P. Taylor, G. Yegin, D. W. O. Rogers",
        "date":"2007",
        "location": "Med. Phys., 34, 445 &mdash; 457",
    },
    {
        "file":"TR08.pdf",
        "title":"More accurate fitting of <sup>125</sup>I and <sup>103</sup>Pd radial dose functions",
        "authors":"R. E. P. Taylor, D. W. O. Rogers",
        "date":"2008",
        "location": "Med. Phys., 35, 4242 &mdash; 4250",
    },
    {
        "file":"TR08b.pdf",
        "title":"An EGSnrc Monte Carlo-calculated database of TG-43 parameters",
        "authors":"R. E. P. Taylor, D. W. O. Rogers",
        "date":"2008",
        "location": "Med. Phys., 35, 4228 &mdash; 4241",
    },
    {
        "file":"TR08c.pdf",
        "title":"EGSnrc Monte Carlo calculated dosimetry parameters for 192Ir and 169Yb brachytherapy sources",
        "authors":"R. E. P. Taylor, D. W. O. Rogers",
        "date":"2008",        
        "location": "Med. Phys., 35, 4933 &mdash; 4944",
    },

    {
        "url":"http://people.physics.carleton.ca/~drogers/pubs/papers/Th08.pdf",
        "title":"Monte Carlo dosimetry for I and Pd eye plaque brachytherapy",
        "authors":"R. M. Thomson, R. E. P. Taylor and D. W. O. Rogers",
        "date":"2008",
        "location": "Med. Phys., 35, 5530 &mdash; 5543",
    },    
]
papers["Conference Presentations"] = [
    {
        "file":"qatrackplus_comp_ws_2013.pdf",
        "title":"QATrack+: A free and open source tool for radiotherapy quality assurance",
        "authors":"R. E. Taylor, C. Angers, D. La Russa, R. Studinski, D. Mason, B. Clark",
        "date":"2013",
        "location": "COMP Winter School, Mt. Tremblant, Quebec",
    },        
    
    {
        "file":"rataylor_mcgill_bd.pdf",
        "title":"An EGSnrc generated TG-43 dosimetry parameter database",
        "authors":"R E P Taylor and D W O Rogers",
        "date":"2007",
        "location": "Monte Carlo Workshop, McGill University",
    },        
    
    {
        "file":"aapm_final_rtaylor.pdf",
        "url":"http://online.medphys.org/resource/1/mphya6/v33/i6/p2205_s4",
        "title":"Monte Carlo Modeling of the Xoft AXXENT X-Ray Source",
        "authors":"R E P Taylor, G Yegin, and D W O Rogers",
        "date":"2006",
        "location": "AAPM 48<sup>th</sup> Annual Meeting, Orland, Florida",
    },        
    
    
]

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
        "last_post":None if not pages else [x for x in sorted(pages,key=lambda p: p.meta["date"])][-1]
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
    return render_template("papers_talks.html",papers=papers)


@app.route("/robots.txt")
def robots():
    return Response(render_template("robots.txt"),mimetype="text/plain")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

    
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)