from fabric.api import *

env.hosts = ['45.76.105.132']
env.user = 'root'
env.password = ',fC1y!2ar.zzV$U='
env.activate = 'source venv/bin/activate && source .env'


def install():
    run('rm -rf JongroDist')
    run('git clone https://github.com/DanielTimLee/JongroDist')
    with cd('~/JongroDist/'):
        run('virtualenv --python=python3 venv')
        with prefix(env.activate):
            run('pip install -r requirements.txt')
            run('bower install --allow-root')
            run('python server.py')


def deploy():
    with cd('~/JongroDist/'):
        run('git checkout preview')
        run('git pull origin preview')
        with prefix(env.activate):
            run('pip install -r requirements.txt')
            run('bower install --allow-root')


def register_upstart():
    sudo('rm -f /etc/init/jongrodist.service')
    sudo('ln -s /home/ubuntu/jongrodist/jongrodist.upstart.service /etc/init/jongrodist.upstart')
    sudo('initctl reload-configuration')


def start():
    sudo('initctl start jongrodist.upstart')


def stop():
    sudo('initctl stop jongrodist.upstart')


def status():
    sudo('initctl status jongrodist.upstart')


def proxy_start():
    sudo('service nginx start')


def proxy_stop():
    sudo('service nginx stop')
