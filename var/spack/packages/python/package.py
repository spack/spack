from spack import *
import os

class Python(Package):
    """The Python programming language."""
    homepage = "http://www.python.org"
    url      = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz"

    extendable = True

    version('2.7.8', 'd235bdfa75b8396942e360a70487ee00')

    depends_on("openssl")
    depends_on("bzip2")
    depends_on("readline")
    depends_on("ncurses")
    depends_on("sqlite")

    def install(self, spec, prefix):
        # Need this to allow python build to find the Python installation.
        env['PYTHONHOME'] = prefix

        # Rest of install is pretty standard.
        configure("--prefix=%s" % prefix,
                  "--with-threads",
                  "--enable-shared")
        make()
        make("install")


    @property
    def python_lib_dir(self):
        return os.path.join('lib', 'python%d.%d' % self.version[:2])


    @property
    def site_packages_dir(self):
        return os.path.join(self.python_lib_dir, 'site-packages')


    def setup_extension_environment(self, module, spec, ext_spec):
        """Called before python modules' install() methods.

        In most cases, extensions will only need to have one line::

            python('setup.py', 'install', '--prefix=%s' % prefix)
        """
        # Python extension builds can have a global python executable function
        module.python = Executable(join_path(spec.prefix.bin, 'python'))

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir = os.path.join(ext_spec.prefix, self.python_lib_dir)
        module.site_packages_dir = os.path.join(ext_spec.prefix, self.site_packages_dir)

        # Add site packages directory to the PYTHONPATH
        os.environ['PYTHONPATH'] = module.site_packages_dir

        # Make the site packages directory if it does not exist already.
        mkdirp(module.site_packages_dir)


    def add_ignore_files(self, args):
        """Add some ignore files to activate/deactivate args."""
        ignore  = set(args.get('ignore', ()))
        ignore.add(os.path.join(self.site_packages_dir, 'site.py'))
        ignore.add(os.path.join(self.site_packages_dir, 'site.pyc'))
        args.update(ignore=ignore)


    def activate(self, ext_pkg, **args):
        self.add_ignore_files(args)
        super(Python, self).activate(ext_pkg, **args)


    def deactivate(self, ext_pkg, **args):
        self.add_ignore_files(args)
        super(Python, self).deactivate(ext_pkg, **args)
