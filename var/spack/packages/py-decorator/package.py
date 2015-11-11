from spack import *

class PyDecorator(Package):
    """Better living through Python with decorators"""
    homepage = "https://github.com/micheles/decorator"
    version("4.0.4", "dd3a0669e1e6f09699eefa2c7fbd9756",
            url="https://pypi.python.org/packages/source/d/decorator/decorator-4.0.4.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
