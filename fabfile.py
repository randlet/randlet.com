from fabric.api import run, env, cd, local


env.hosts = ['randlet.com']

def deploy():
    local("git push origin master")
    venv = "source ~/venvs/randlet.com/bin/activate && "
    with cd("~/projects/randlet.com"):
        run("git pull origin master")
        run(venv + "python sitebuilder.py build")




