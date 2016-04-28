from spack import *

class PyPyyaml(Package):
    """PyYAML is a YAML parser and emitter for Python."""
    homepage = "http://pyyaml.org/wiki/PyYAML"
    url      = "http://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz"

    version('3.11', 'f50e08ef0fe55178479d3a618efe21db')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
