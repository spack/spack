from spack import *

class PyScikitLearn(Package):
    """"""
    homepage = "https://pypi.python.org/pypi/scikit-learn"
    url      = "https://pypi.python.org/packages/source/s/scikit-learn/scikit-learn-0.15.2.tar.gz"

    version('0.15.2', 'd9822ad0238e17b382a3c756ea94fe0d')
    version('0.16.1', '363ddda501e3b6b61726aa40b8dbdb7e')

    extends('python')
    depends_on('python@2.7.10')
    depends_on('py-numpy@1.9.2')
    depends_on('py-scipy@0.15.1')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
