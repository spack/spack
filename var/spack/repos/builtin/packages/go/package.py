import os
import shutil
import glob
import llnl.util.tty as tty
from spack import *


class Go(Package):
    """The golang compiler and build environment"""
    homepage = "https://golang.org"
    url = "https://go.googlesource.com/go"

    extendable = True

    version('1.5.4', git='https://go.googlesource.com/go', tag='go1.5.4')
    version('1.6.2', git='https://go.googlesource.com/go', tag='go1.6.2')

    variant('test',
            default=True,
            description="Run tests as part of build, a good idea but quite"
            " time consuming")

    provides('golang')

    # to-do, make non-c self-hosting compilers feasible without backflips
    # should be a dep on external go compiler
    depends_on('go-bootstrap')
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
        spack_env.set('GOROOT_BOOTSTRAP', self.spec['go-bootstrap'].prefix)

    def setup_dependent_package(self, module, ext_spec):
        """Called before go modules' install() methods.

        In most cases, extensions will only need to set GOPATH and use go::

        env = os.environ
        env['GOPATH'] = self.source_path + ':' + env['GOPATH']
        go('get', '<package>', env=env)
        shutil.copytree('bin', os.path.join(prefix, '/bin'))
        """
        #  Add a go command/compiler for extensions
        module.go = Executable(join_path(self.spec.prefix.bin, 'go'))

    def setup_dependent_environment(self, spack_env, run_env, ext_spec):
        if os.environ.get('GOROOT', False):
            tty.warn('GOROOT is set, this is not recommended')

        path_components = []
        # Set GOPATH to include paths of dependencies
        for d in ext_spec.traverse():
            if d.package.extends(self.spec):
                path_components.append(d.prefix)

        # This *MUST* be first, this is where new code is installed
        spack_env.set('GOPATH', ':'.join(path_components))

        # Allow packages to find this when using module or dotkit
        run_env.prepend_path('GOPATH', ':'.join(
            [ext_spec.prefix] + path_components))
