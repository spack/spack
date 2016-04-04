from spack import *

class PyDask(Package):
    """Minimal task scheduling abstraction"""
    homepage = "https://github.com/dask/dask/"
    url      = "https://pypi.python.org/packages/source/d/dask/dask-0.8.1.tar.gz"

    version('0.8.1', '5dd8e3a3823b3bc62c9a6d192e2cb5b4')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
