from spack import *

class PyPychecker(Package):
    """"""
    homepage = "http://pychecker.sourceforge.net/"
    url      = "http://sourceforge.net/projects/pychecker/files/pychecker/0.8.19/pychecker-0.8.19.tar.gz"

    version('0.8.19', 'c37182863dfb09209d6ba4f38fce9d2b')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
