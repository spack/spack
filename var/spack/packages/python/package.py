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


    def setup_extension_environment(self, module, spec, ext_spec):
        """Called before python modules' install() methods.

        In most cases, extensions will only need to have one line::

            python('setup.py', 'install', '--prefix=%s' % prefix)
        """
        # Python extension builds can have a global python executable function
        module.python = Executable(join_path(spec.prefix.bin, 'python'))

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir = join_path(ext_spec.prefix.lib, 'python%d.%d' % self.version[:2])
        module.site_packages_dir = join_path(module.python_lib_dir, 'site-packages')

        # Add site packages directory to the PYTHONPATH
        os.environ['PYTHONPATH'] = module.site_packages_dir

        # Make the site packages directory if it does not exist already.
        mkdirp(module.site_packages_dir)
