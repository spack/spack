from spack import *

class PyGenshi(Package):
    """Python toolkit for generation of output for the web"""
    homepage = "https://genshi.edgewall.org/"
    url      = "http://ftp.edgewall.com/pub/genshi/Genshi-0.7.tar.gz"

    version('0.7'  , '54e64dd69da3ec961f86e686e0848a82')
    version('0.6.1', '372c368c8931110b0a521fa6091742d7')
    version('0.6'  , '604e8b23b4697655d36a69c2d8ef7187')

    extends("python")
    depends_on("py-setuptools")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
