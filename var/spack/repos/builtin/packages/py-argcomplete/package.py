from spack import *

class PyArgcomplete(Package):
    """Bash tab completion for argparse."""

    homepage = "https://pypi.python.org/pypi/argcomplete"
    url      = "https://pypi.python.org/packages/source/a/argcomplete/argcomplete-1.1.0.tar.gz"

    version('1.1.0', '07504963b54e6af8aa8c51a4913bbbe3')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
