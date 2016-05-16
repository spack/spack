from spack import *
import os
import shutil


class ThePlatinumSearcher(Package):
    """Fast parallel recursive grep alternative"""
    homepage = "https://github.com/monochromegane/the_platinum_searcher"
    url = "https://github.com/monochromegane/the_platinum_searcher"

    package = 'github.com/monochromegane/the_platinum_searcher/...'

    version('head', go=package)

    extends("go")

    def install(self, spec, prefix):
        go('install', self.package)
        shutil.copytree('bin', os.path.join(prefix, 'bin'))
