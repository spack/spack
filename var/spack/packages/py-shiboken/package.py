from spack import *

class PyShiboken(Package):
    """Shiboken generates bindings for C++ libraries using CPython source code."""
    homepage = "https://shiboken.readthedocs.org/"
    url      = "https://pypi.python.org/packages/source/S/Shiboken/Shiboken-1.2.2.tar.gz"

    version('1.2.2', '345cfebda221f525842e079a6141e555')

    # TODO: make build dependency
    # depends_on("cmake")

    extends('python')
    depends_on("py-setuptools")
    depends_on("libxml2")
    depends_on("qt@:4.8")

    def install(self, spec, prefix):
        python('setup.py', 'install',
               '--prefix=%s' % prefix,
               '--jobs=%s' % make_jobs)
