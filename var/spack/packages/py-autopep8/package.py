from spack import *

class PyAutopep8(Package):
    """A tool that automatically formats Python code to conform to the PEP 8 style guide"""
    homepage = "https://github.com/hhatto/autopep8"
    version("1.1", "7998358d8f0efd77dcb2cc8e34e3cb5c",
            url="https://pypi.python.org/packages/source/a/autopep8/autopep8-1.1.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
