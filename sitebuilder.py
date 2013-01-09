import collections
import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.context_processor
def inject_tags():
    tags = []
    for p in pages:
        tags.extend(p.meta.get('tags',[]))
    tags = [x[0] for x in collections.Counter(tags).most_common(10)]
    return {"tags":tags}

@app.route('/')
def index():
    most_recent = pages
    return render_template('index.html', pages=pages)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)

@app.route('/projects/')
def projects():
    return render_template('index.html', pages=pages)

@app.route('/blog/')
def  blog():
    return render_template('index.html', pages=pages)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)