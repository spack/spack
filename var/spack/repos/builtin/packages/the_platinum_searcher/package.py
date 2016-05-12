from spack import *

class ThePlatinumSearcher(Package):
    """Fast parallel recursive grep alternative"""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "https://github.com/monochromegane/the_platinum_searcher"
    url      = "https://github.com/monochromegane/the_platinum_searcher/archive/v1.7.7.tar.gz"

    version('1.7.7', '08d7265e101bc1427d5d4b9903aa1166')

    depends_on("go")

    def install(self, spec, prefix):
        env = which('env')
        env()
        # Fetch all dependencies
        go('get', './...')
        # Build pt
        go('build')
