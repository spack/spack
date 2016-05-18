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
        env = os.environ
        env['GOPATH'] = self.stage.source_path + ':' + env['GOPATH']
        go('install', self.package, env=env)
        shutil.copytree('bin', os.path.join(prefix, 'bin'))
