import os
import shutil
import glob
from spack import *


class Go(Package):
    """The golang compiler and build environment"""
    homepage = "https://golang.org"
    url = "https://go.googlesource.com/go"

    extendable = True

    # temporary fix until tags are pulled correctly
    version('1.4.2', git='https://go.googlesource.com/go', tag='go1.4.2')
    version('1.5.4', git='https://go.googlesource.com/go', tag='go1.5.4')
    version('1.6.2', git='https://go.googlesource.com/go', tag='go1.6.2')

    variant('test',
            default=True,
            description="Run tests as part of build, a good idea but quite"
            " time consuming")

    provides('golang')

    # to-do, make non-c self-hosting compilers feasible without backflips
    # should be go_compiler, but that creates an infinite loop
    depends_on('gcc@5:', when='@1.5:')
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
        # spack_env.set("GOROOT", self.spec.prefix)
        # run_env.set("GOROOT", self.spec.prefix)
        spack_env.set('GOROOT_FINAL', self.spec.prefix)
        spack_env.set('GOROOT_BOOTSTRAP', self.spec['gcc'].prefix)

    def setup_dependent_package(self, module, ext_spec):
        #  Add a go command/compiler for extensions
        module.go = Executable(join_path(self.spec.prefix.bin, 'go'))

    def setup_dependent_environment(self, spack_env, run_env, ext_spec):
        """Called before go modules' install() methods.

        In most cases, extensions will only need to have two lines::

        go('get', '<package>')
        shutil.copytree('bin', os.path.join(prefix, '/bin'))
        """

        if os.environ.get('GOROOT', False):
            tty.warn('GOROOT is set, this is not recommended')

        # Set GOPATH to include paths of dependencies
        for d in extension_spec.traverse():
            if d.package.extends(self.spec):
                spack_env.prepend_path('GOPATH', d.prefix)

        # This *MUST* be first, this is where new code is installed
        spack_env.prepend_path('GOPATH', ext_spec.package.stage.source_path)

        # Allow packages to find this when using module or dotkit
        run_env.prepend_path('GOPATH', ext_spec.prefix)
