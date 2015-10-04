from spack import *

class PyDistutils2(Package):
    """Python Packaging Library."""
    
    homepage = "https://hg.python.org/distutils2"
    url      = "https://pypi.python.org/packages/source/D/Distutils2/Distutils2-1.0a4.tar.gz"

    version('1.0a4', '52bc9dffb394970c27e02853ae3a3241')

    depends_on("python")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

