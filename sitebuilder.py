import collections
import datetime
import itertools
import json
import sys
import PyRSS2Gen
from flask import Flask, Response, render_template, abort, url_for
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from jinja2 import Markup

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
sorted_pages = sorted(pages, key=lambda p: p.meta["date"], reverse=True)

freezer = Freezer(app)


valid_projects = collections.OrderedDict()
for proj in json.load(open("config/projects.json")):
    proj['description'] = Markup(proj['description'])
    valid_projects[proj['slug']] = proj


papers = collections.OrderedDict()
papers["Papers"] = json.load(open("config/papers.json"))
papers["Talks & Conference Presentations"] = json.load(open("config/presentations.json"))
papers["M.Sc. Thesis"] = json.load(open("config/thesis.json"))


@app.context_processor
def inject_tags():
    tags = []
    for p in pages:
        tags.extend(p.meta.get('tags', []))
    tags = [x[0] for x in collections.Counter(tags).most_common(10)]
    return {"tags": tags}


@app.route('/')
def index():
    context = {
        "page_title": "Programming, Science &amp; Life",
        "pages": sorted_pages,
        "last_post": None if not pages else list(sorted_pages)[0]
    }
    return render_template('index.html', **context)


def pages_by_tag(tag):
    return [p for p in sorted_pages if tag in p.meta.get('tags', [])]


@app.route('/tag/<string:tag>/')
def tag(tag):
    return render_template('tag.html', pages=pages_by_tag(tag), tag=tag)


@app.route('/projects/')
def projects():
    return render_template('projects/index.html', projects=valid_projects)


@app.route('/projects/<path:project>/')
def project(project):

    if project not in valid_projects:
        abort(404)
    return render_template("projects/%s/index.html" % project, project=valid_projects[project], project_id=project)


@app.route('/projects/<path:project>/<path:subpage>/')
def project_subpage(project, subpage):
    return render_template("projects/%s/%s.html" % (project, subpage), project=valid_projects[project])


@app.route('/blog/')
def blog():
    return render_template('blog.html', pages=sorted_pages)


@app.route('/blog/rss.xml')
@app.route('/blog/<tag>/rss.xml')
def posts_feed(tag=None):

    filtered_pages = sorted_pages
    if tag is not None:
        filtered_pages = pages_by_tag(tag)

    rss = PyRSS2Gen.RSS2(
        title="Randle Taylor's Blog Feed",
        link="http://randlet.com/blog/rss/",
        description="Posts on programming and general technology with a focus on Python & web applications",

        lastBuildDate=datetime.datetime.now(),
        items=[
            PyRSS2Gen.RSSItem(
                title=page.meta.get("title", "Untitled"),
                link="http://randlet.com/blog/%s/" % (page.path),
                description=page.meta.get("blurb", ""),
                guid=PyRSS2Gen.Guid(page.path),
                pubDate=page.meta.get("date").strftime("%a, %d %b %Y %H:%M:%S %z")
            ) for page in filtered_pages
        ]
    )

    return Response(rss.to_xml(), mimetype="text/xml")


@freezer.register_generator
def posts_feed():
    #url generator for filtered  xml pages
    all_tags = (itertools.chain(*(p.meta.get("tags", []) for p in pages)))
    for tag in all_tags:
        yield {'tag': tag}


@app.route('/blog/<path:path>/')
def posts(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


@app.route('/papers-talks/')
def papers_talks():
    return render_template("papers_talks.html",papers=papers)


@app.route('/hire-me/')
def hire_me():
    return render_template("hire_me.html")


@app.route("/robots.txt")
def robots():
    return Response(render_template("robots.txt"),mimetype="text/plain")


@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}


def urlf(url):
    remove = ["img", "js", "style", "font"]
    return not any(url.startswith("/static/%s" % x) for x in remove)


other_urls = list([u for u in freezer.all_urls() if urlf(u)])
page_urls = ["/blog/%s" % p.path for p in pages]


@app.route('/sitemap.xml')
def sitemap():
    url_root = r"http://randlet.com"
    rules = page_urls + other_urls
    return Response(render_template('sitemap.xml', url_root=url_root, rules=rules),mimetype="text/xml" )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        use_reloader = len(sys.argv) > 1 and sys.argv[1] == "reload"

        app.run(port=8000, use_reloader=use_reloader)
