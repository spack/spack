from spack import *

class GitTest(Package):
    """Mock package that uses git for fetching."""
    homepage = "http://www.git-fetch-example.com"

    version('git', git='to-be-filled-in-by-test')

    def install(self, spec, prefix):
        pass
