from spack import *

class PyPygments(Package):
    """Pygments is a syntax highlighting package written in Python."""
    homepage = "https://pypi.python.org/pypi/pygments"
    url      = "https://pypi.python.org/packages/source/P/Pygments/Pygments-2.0.1.tar.gz"

    version('2.0.1', 'e0daf4c14a4fe5b630da765904de4d6c')
    version('2.0.2', '238587a1370d62405edabd0794b3ec4a')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
