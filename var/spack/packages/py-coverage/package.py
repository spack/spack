from spack import *

class PyCoverage(Package):
    """ Testing coverage checker for python """
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://nedbatchelder.com/code/coverage/"
    url      = "https://pypi.python.org/packages/source/c/coverage/coverage-4.0a6.tar.gz"

    version('4.0a6', '1bb4058062646148965bef0796b61efc')

    depends_on('py-setuptools')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
