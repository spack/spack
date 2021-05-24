from spack import *


class PyPysph(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    url      = "https://github.com/pypr/pysph.git"

     maintainers = ['samcom12']


    def install(self, spec, prefix):
        make()
        make('install')
