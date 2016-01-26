from spack import *

class HgTest(Package):
    """Test package that does fetching with mercurial."""
    homepage = "http://www.hg-fetch-example.com"

    version('hg', hg='to-be-filled-in-by-test')

    def install(self, spec, prefix):
        pass
