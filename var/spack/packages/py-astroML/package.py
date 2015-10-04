from spack import *

class PyAstroml(Package):
    """tools for machine learning and data mining in Astronomy"""
    homepage = "http://astroML.github.com"
    version("0.2", "85f558368546660564f20b30efafb024",
            url="https://pypi.python.org/packages/source/a/astroML/astroML-0.2.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
