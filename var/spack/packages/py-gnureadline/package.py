from spack import *

class PyGnureadline(Package):
    """The standard Python readline extension statically linked against the GNU readline library."""
    homepage = "http://github.com/ludwigschwardt/python-gnureadline"
    version("6.3.3", "c4af83c9a3fbeac8f2da9b5a7c60e51c",
            url="https://pypi.python.org/packages/source/g/gnureadline/gnureadline-6.3.3.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
