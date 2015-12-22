import os
import re
from contextlib import closing
from llnl.util.lang import match_predicate
from spack.util.environment import *

from spack import *
import spack


class Python(Package):
    """The Python programming language."""
    homepage = "http://www.python.org"
    url      = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz"

    extendable = True

    version('2.7.8', 'd235bdfa75b8396942e360a70487ee00')
    version('2.7.10', 'c685ef0b8e9f27b5e3db5db12b268ac6')
    version('2.7.11', '1dbcc848b4cd8399a8199d000f9f823c', preferred=True)
    version('3.5.0', 'd149d2812f10cbe04c042232e7964171')
    version('3.5.1', 'e9ea6f2623fffcdd871b7b19113fde80')

    depends_on("openssl")
    depends_on("bzip2")
    depends_on("readline")
    depends_on("ncurses")
    depends_on("sqlite")
    depends_on("zlib")

    def install(self, spec, prefix):
        # Need this to allow python build to find the Python installation.
        env['PYTHONHOME'] = prefix
        env['MACOSX_DEPLOYMENT_TARGET'] = '10.6'

        # Rest of install is pretty standard except setup.py needs to be able to read the CPPFLAGS
        # and LDFLAGS as it scans for the library and headers to build
        configure_args= [
                  "--prefix=%s" % prefix,
                  "--with-threads",
                  "--enable-shared",
                  "CPPFLAGS=-I%s/include -I%s/include -I%s/include -I%s/include -I%s/include -I%s/include" % (
                       spec['openssl'].prefix, spec['bzip2'].prefix,
                       spec['readline'].prefix, spec['ncurses'].prefix,
                       spec['sqlite'].prefix, spec['zlib'].prefix),
                  "LDFLAGS=-L%s/lib -L%s/lib -L%s/lib -L%s/lib -L%s/lib -L%s/lib" % (
                       spec['openssl'].prefix, spec['bzip2'].prefix,
                       spec['readline'].prefix, spec['ncurses'].prefix,
                       spec['sqlite'].prefix, spec['zlib'].prefix)
                  ]
        if spec.satisfies('@3:'):
            configure_args.append('--without-ensurepip')
        configure(*configure_args)
        make()
        make("install")


    # ========================================================================
    # Set up environment to make install easy for python extensions.
    # ========================================================================

    @property
    def python_lib_dir(self):
        return os.path.join('lib', 'python%d.%d' % self.version[:2])


    @property
    def python_include_dir(self):
        return os.path.join('include', 'python%d.%d' % self.version[:2])


    @property
    def site_packages_dir(self):
        return os.path.join(self.python_lib_dir, 'site-packages')


    def setup_dependent_environment(self, module, spec, ext_spec):
        """Called before python modules' install() methods.

        In most cases, extensions will only need to have one line::

            python('setup.py', 'install', '--prefix=%s' % prefix)
        """
        # Python extension builds can have a global python executable function
        if self.version >= Version("3.0.0") and self.version < Version("4.0.0"):
            module.python = Executable(join_path(spec.prefix.bin, 'python3'))
        else:
            module.python = Executable(join_path(spec.prefix.bin, 'python'))

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir     = os.path.join(ext_spec.prefix, self.python_lib_dir)
        module.python_include_dir = os.path.join(ext_spec.prefix, self.python_include_dir)
        module.site_packages_dir  = os.path.join(ext_spec.prefix, self.site_packages_dir)

        # Make the site packages directory if it does not exist already.
        mkdirp(module.site_packages_dir)

        # Set PYTHONPATH to include site-packages dir for the
        # extension and any other python extensions it depends on.
        python_paths = []
        for d in ext_spec.traverse():
            if d.package.extends(self.spec):
                python_paths.append(os.path.join(d.prefix, self.site_packages_dir))
        os.environ['PYTHONPATH'] = ':'.join(python_paths)


    # ========================================================================
    # Handle specifics of activating and deactivating python modules.
    # ========================================================================

    def python_ignore(self, ext_pkg, args):
        """Add some ignore files to activate/deactivate args."""
        ignore_arg = args.get('ignore', lambda f: False)

        # Always ignore easy-install.pth, as it needs to be merged.
        patterns = [r'easy-install\.pth$']

        # Ignore pieces of setuptools installed by other packages.
        if ext_pkg.name != 'py-setuptools':
            patterns.append(r'/site[^/]*\.pyc?$')
            patterns.append(r'setuptools\.pth')
            patterns.append(r'bin/easy_install[^/]*$')
            patterns.append(r'setuptools.*egg$')

        return match_predicate(ignore_arg, patterns)


    def write_easy_install_pth(self, exts):
        paths = []
        for ext in sorted(exts.values()):
            ext_site_packages = os.path.join(ext.prefix, self.site_packages_dir)
            easy_pth = "%s/easy-install.pth" % ext_site_packages

            if not os.path.isfile(easy_pth):
                continue

            with closing(open(easy_pth)) as f:
                for line in f:
                    line = line.rstrip()

                    # Skip lines matching these criteria
                    if not line: continue
                    if re.search(r'^(import|#)', line): continue
                    if (ext.name != 'py-setuptools' and
                        re.search(r'setuptools.*egg$', line)): continue

                    paths.append(line)

        site_packages = os.path.join(self.prefix, self.site_packages_dir)
        main_pth = "%s/easy-install.pth" % site_packages

        if not paths:
            if os.path.isfile(main_pth):
                os.remove(main_pth)

        else:
            with closing(open(main_pth, 'w')) as f:
                f.write("import sys; sys.__plen = len(sys.path)\n")
                for path in paths:
                    f.write("%s\n" % path)
                f.write("import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; "
                        "p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)\n")


    def activate(self, ext_pkg, **args):
        ignore=self.python_ignore(ext_pkg, args)
        args.update(ignore=ignore)

        super(Python, self).activate(ext_pkg, **args)

        exts = spack.install_layout.extension_map(self.spec)
        exts[ext_pkg.name] = ext_pkg.spec
        self.write_easy_install_pth(exts)


    def deactivate(self, ext_pkg, **args):
        args.update(ignore=self.python_ignore(ext_pkg, args))
        super(Python, self).deactivate(ext_pkg, **args)

        exts = spack.install_layout.extension_map(self.spec)
        if ext_pkg.name in exts:        # Make deactivate idempotent.
            del exts[ext_pkg.name]
            self.write_easy_install_pth(exts)
