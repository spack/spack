from spack import *

class PyAstropy(Package):
    """Community-developed python astronomy tools"""
    homepage = "http://astropy.org"
    version("0.4.2", "6dc4f643cde37ba0a8b4967dc8becee8",
            url="https://pypi.python.org/packages/source/a/astropy/astropy-0.4.2.tar.gz")

    extends("python")
    depends_on("py-numpy")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
