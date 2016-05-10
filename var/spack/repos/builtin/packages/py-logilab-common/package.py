from spack import *

class PyLogilabCommon(Package):
    """Common modules used by Logilab projects"""
    homepage = "https://www.logilab.org/project/logilab-common"
    url      = "https://pypi.python.org/packages/a7/31/1650d23e44794d46935d82b86e73454cc83b814cbe1365260ccce8a2f4c6/logilab-common-1.2.0.tar.gz"

    version('1.2.0', 'f7b51351b7bfe052746fa04c03253c0b')

    extends("python")
    depends_on("py-setuptools")
    depends_on("py-six")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

