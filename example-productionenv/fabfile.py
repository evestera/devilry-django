from os.path import exists
from os import remove
from fabric.api import local, abort, task



@task
def setup_demo():
    """
    Runs ``reset``, ``remove_db`` and ``autodb`` tasks.
    """
    reset()
    autodb()


@task
def virtualenv():
    """
    Setup a virtualenv in virtualenv/, run bootstrap in the virtualenv, and run bootstrap.
    """
    local('virtualenv virtualenv')
    local('virtualenv/bin/python ../bootstrap.py')
    local('bin/buildout')

@task
def clean():
    print('Are you sure you want to completely reset the environment? This '
          'will run "git clean -dfx .", which removes any '
          'untracked files in this directory:')
    local('git clean -ndfx .')
    ok = raw_input('Proceed (y/N)? ')
    if ok != 'y':
        abort('Aborted')
    local('git clean -dfx .')

@task
def syncdb():
    local('bin/django_dev.py syncdb -v0 --noinput')

@task
def autogen_extjsmodels():
    local('bin/django_dev.py dev_autogen_extjsmodels')

@task
def reset():
    clean()
    virtualenv()
    autogen_extjsmodels()

@task
def autodb():
    syncdb()
    local('bin/django_dev.py dev_autodb -v2')
