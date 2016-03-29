from spack import *


class Ruby(Package):
    """A dynamic, open source programming language with a focus on
    simplicity and productivity."""

    homepage = "https://www.ruby-lang.org/"
    url      = "http://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz"

    extendable = True

    version('2.2.0', 'cd03b28fd0b555970f5c4fd481700852')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")

    def setup_dependent_environment(self, spack_env, run_env, extension_spec):
        # TODO: do this only for actual extensions.
        # Set GEM_PATH to include dependent gem directories
        ruby_paths = []
        for d in extension_spec.traverse():
            if d.package.extends(self.spec):
                ruby_paths.append(d.prefix)

        spack_env.set_path('GEM_PATH', ruby_paths)

        # The actual installation path for this gem
        spack_env.set('GEM_HOME', extension_spec.prefix)

    def setup_dependent_package(self, module, ext_spec):
        """Called before ruby modules' install() methods.  Sets GEM_HOME
        and GEM_PATH to values appropriate for the package being built.

        In most cases, extensions will only need to have one line::

            gem('install', '<gem-name>.gem')
        """
        # Ruby extension builds have global ruby and gem functions
        module.ruby = Executable(join_path(self.spec.prefix.bin, 'ruby'))
        module.gem = Executable(join_path(self.spec.prefix.bin, 'gem'))
