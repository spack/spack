from spack import *

class PyJsonschema(Package):
    """implementation of JSON Schema validation for Python"""
    homepage = "https://github.com/Julian/jsonschema"
    url      = "https://pypi.python.org/packages/source/j/jsonschema/jsonschema-2.5.1.tar.gz"

    version('2.4.0','661f85c3d23094afbb9ac3c0673840bf',
           url='https://pypi.python.org/packages/source/j/jsonschema/jsonschema-2.4.0.tar.gz')
    version('2.5.1', '374e848fdb69a3ce8b7e778b47c30640')

    extends("python")
    depends_on("py-setuptools@18.1")
    depends_on("py-vcversioner")
    depends_on("py-functools32")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
