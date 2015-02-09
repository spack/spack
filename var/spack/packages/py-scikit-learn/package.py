from spack import *

class PyScikitLearn(Package):
    """"""
    homepage = "https://pypi.python.org/pypi/scikit-learn"
    url      = "https://pypi.python.org/packages/source/s/scikit-learn/scikit-learn-0.15.2.tar.gz"

    version('0.15.2', 'd9822ad0238e17b382a3c756ea94fe0d')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
