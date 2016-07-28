import os
import shutil
import glob
from spack import *

# THIS PACKAGE SHOULD NOT EXIST
# it exists to make up for the inability to:
# * use an external go compiler
# * have go depend on itself
# * have a sensible way to find gccgo without a dep on gcc


class GoBootstrap(Package):
    """Old C-bootstrapped go to bootstrap real go"""
    homepage = "https://golang.org"
    url = "https://go.googlesource.com/go"

    extendable = True

    # temporary fix until tags are pulled correctly
    version('1.4.2', git='https://go.googlesource.com/go', tag='go1.4.2')

    variant('test',
            default=True,
            description="Run tests as part of build, a good idea but quite"
            " time consuming")

    provides('golang@:1.4.2')

    depends_on('git')

    def install(self, spec, prefix):
        bash = which('bash')
        with working_dir('src'):
            if '+test' in spec:
                bash('all.bash')
            else:
                bash('make.bash')

        try:
            os.makedirs(prefix)
        except OSError:
            pass
        for f in glob.glob('*'):
            if os.path.isdir(f):
                shutil.copytree(f, os.path.join(prefix, f))
            else:
                shutil.copy2(f, os.path.join(prefix, f))

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GOROOT_FINAL', self.spec.prefix)
