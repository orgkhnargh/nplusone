# -*- coding: utf-8 -*-

import os
import sys
import webbrowser

from invoke import run
from invoke import task


docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')


@task
def test():
    import pytest
    errcode = pytest.main(['tests'])
    sys.exit(errcode)


@task
def watch():
    """Run tests when a file changes. Requires pytest-xdist."""
    import pytest
    errcode = pytest.main(['-f'])
    sys.exit(errcode)


@task
def clean():
    run('rm -rf build')
    run('rm -rf dist')
    run('rm -rf nplusone.egg-info')
    clean_docs()
    print('Cleaned up.')


@task
def clean_docs():
    run('rm -rf {0}'.format(build_dir))


@task
def browse_docs():
    path = os.path.join(build_dir, 'index.html')
    webbrowser.open_new_tab(path)


@task
def docs(clean=False, browse=False, watch=False):
    """Build the docs."""
    if clean:
        clean_docs()
    run('sphinx-build {0} {1}'.format(docs_dir, build_dir), pty=True)
    if browse:
        browse_docs()
    if watch:
        watch_docs()


@task
def watch_docs():
    """Run build the docs when a file changes."""
    try:
        import sphinx_autobuild  # noqa
    except ImportError:
        print('ERROR: watch task requires the sphinx_autobuild package.')
        print('Install it with:')
        print('    pip install sphinx-autobuild')
        sys.exit(1)
    docs()
    run('sphinx-autobuild {} {}'.format(docs_dir, build_dir), pty=True)


@task
def readme(browse=False):
    run('rst2html.py README.rst > README.html', pty=True)
    if browse:
        webbrowser.open_new_tab('README.html')


@task
def publish(test=False):
    """Publish to the cheeseshop."""
    try:
        __import__('wheel')
    except ImportError:
        print('wheel required. Run `pip install wheel`.')
        sys.exit(1)
    if test:
        run(
            'python setup.py register -r test sdist bdist_wheel upload -r test',
            echo=True,
        )
    else:
        run('python setup.py register sdist bdist_wheel upload', echo=True)
