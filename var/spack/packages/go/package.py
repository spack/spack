import os
from spack import *

class Go(Package):
    """The golang compiler and build environment"""
    homepage = "https://golang.org"
    url = "https://go.googlesource.com/go"

    extendable = True

    # temporary fix until tags are pulled correctly
    version('1.4.2', git='https://go.googlesource.com/go', tag='go1.4.2')

    # to-do, make non-c self-hosting compilers possible
    # depends_on('go@:1.4.2', when='@1.5:')

    def install(self, spec, prefix):
      os.environ['GOROOT'] = os.getcwd()
      os.environ['GOBIN'] = join_path(os.getcwd(), 'bin')
      os.environ['GOROOT_FINAL'] = prefix
      bash = which('bash')
      bash('-c', 'env')
      bash('-c', 'pwd')
      with working_dir('src'):
        #TODO: crutch until the read-only-filesystem bug is fixed upstream
        bash('all.bash', fail_on_error=False)
      cp = which('cp')
      bash('-c', 'cp -r ./* "{}"'.format(prefix))

    def setup_dependent_environment(self, module, spec, ext_spec):
        """Called before go modules' install() methods.

        In most cases, extensions will only need to have one line::

            go('get', '<package>')
        """
        #  Add a go command for extensions
        module.go = Executable(join_path(spec.prefix.bin, 'go'))
        os.environ['GOROOT'] = spec.prefix

        stage_path = os.path.realpath(ext_spec.package.stage.source_path)
        print "PREFIX: {}".format(stage_path)
        go_paths = [stage_path]
        for d in ext_spec.traverse():
            if d.package.extends(self.spec):
                go_paths.append(d.prefix)
        os.environ['GOPATH'] = ':'.join(go_paths)


