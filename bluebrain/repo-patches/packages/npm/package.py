from spack import *
from spack.pkg.builtin.npm import Npm as BuiltinNpm


class Npm(BuiltinNpm):
    version('7.0.11', sha256='5ca03029c81af0bcb2de7a7ff05e4d0edda38dcee13f6a4773c1efe810b3378f')

    # node did not seem to be able to find all modules in parallel make
    parallel = False

    def install(self, spec, prefix):
        if spec.satisfies('@:6.999'):
            make('install')
        else:
            # manually re-instate code of the old install target
            mkdir(prefix.lib)
            node = spack.util.executable.which('node')
            node('bin/npm-cli.js', 'pack')
            node('bin/npm-cli.js', 'install', '-g', '-f',
                 'npm-{0}.tgz'.format(spec.version))
