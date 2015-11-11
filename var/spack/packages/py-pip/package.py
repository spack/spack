from spack import *

class PyPip(Package):
    """The PyPA recommended tool for installing Python packages."""
    homepage = "https://pip.pypa.io/"
    version("7.1.2", "3823d2343d9f3aaab21cf9c917710196",
            url="https://pypi.python.org/packages/source/p/pip/pip-7.1.2.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
