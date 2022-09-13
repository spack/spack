from spack import *

class LibpressioErrorinjector(CMakePackage):
    """LibPressioErrorInjector injects errors in to data for sensitivity studies"""

    homepage = "https://github.com/robertu94/libpressio-errorinjector"
    git      = "git@github.com:robertu94/libpressio-errorinjector.git"

    maintainers = ['robertu94']

    version('master', branch="master")

    depends_on('libpressio')

    def cmake_args(self):
        args = []
        return args
