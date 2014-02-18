from fabric.api import run, env, cd


env.hosts = ['randlet.com']

def deploy():
    venv = "source ~/venvs/randlet.com/bin/activate && "
    with cd("~/projects/randlet.com"):
        run("git pull origin master")
        run(venv + "python sitebuilder.py build")




