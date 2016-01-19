from spack import *

class SvnTest(Package):
    """Mock package that uses svn for fetching."""
    url      = "http://www.example.com/svn-test-1.0.tar.gz"

    version('svn', 'to-be-filled-in-by-test')

    def install(self, spec, prefix):
        pass
