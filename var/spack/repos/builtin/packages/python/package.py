##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import ast
import os
import platform
import re
import sys

import llnl.util.tty as tty
from llnl.util.lang import match_predicate
from llnl.util.filesystem import (force_remove, get_filetype,
                                  path_contains_subdirectory)

import spack.store
import spack.util.spack_json as sjson
from spack.util.environment import is_system_path
from spack.util.prefix import Prefix
from spack import *


class Python(AutotoolsPackage):
    """The Python programming language."""

    homepage = "http://www.python.org"
    url = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz"
    list_url = "https://www.python.org/downloads/"
    list_depth = 1

    version('3.7.0', '41b6595deb4147a1ed517a7d9a580271')
    version('3.6.5', 'ab25d24b1f8cc4990ade979f6dc37883')
    version('3.6.4', '9de6494314ea199e3633211696735f65')
    version('3.6.3', 'e9180c69ed9a878a4a8a3ab221e32fa9')
    version('3.6.2', 'e1a36bfffdd1d3a780b1825daf16e56c')
    version('3.6.1', '2d0fc9f3a5940707590e07f03ecb08b9')
    version('3.6.0', '3f7062ccf8be76491884d0e47ac8b251')
    version('3.5.2', '3fe8434643a78630c61c6464fe2e7e72')
    version('3.5.1', 'be78e48cdfc1a7ad90efff146dce6cfe')
    version('3.5.0', 'a56c0c0b45d75a0ec9c6dee933c41c36')
    version('3.4.3', '4281ff86778db65892c05151d5de738d')
    version('3.3.6', 'cdb3cd08f96f074b3f3994ccb51063e9')
    version('3.2.6', '23815d82ae706e9b781ca65865353d39')
    version('3.1.5', '02196d3fc7bc76bdda68aa36b0dd16ab')
    version('2.7.15', '045fb3440219a1f6923fefdabde63342', preferred=True)
    version('2.7.14', 'cee2e4b33ad3750da77b2e85f2f8b724')
    version('2.7.13', '17add4bf0ad0ec2f08e0cae6d205c700')
    version('2.7.12', '88d61f82e3616a4be952828b3694109d')
    version('2.7.11', '6b6076ec9e93f05dd63e47eb9c15728b')
    version('2.7.10', 'd7547558fd673bd9d38e2108c6b42521')
    version('2.7.9', '5eebcaa0030dc4061156d3429657fb83')
    version('2.7.8', 'd4bca0159acb0b44a781292b5231936f')

    extendable = True

    # --enable-shared is known to cause problems for some users on macOS
    # See http://bugs.python.org/issue29846
    variant('shared', default=sys.platform != 'darwin',
            description='Enable shared libraries')
    variant('tk', default=False, description='Provide support for Tkinter')
    variant('ucs4', default=False,
            description='Enable UCS4 (wide) unicode strings')
    # From https://docs.python.org/2/c-api/unicode.html: Python's default
    # builds use a 16-bit type for Py_UNICODE and store Unicode values
    # internally as UCS2. It is also possible to build a UCS4 version of Python
    # (most recent Linux distributions come with UCS4 builds of Python).  These
    # builds then use a 32-bit type for Py_UNICODE and store Unicode data
    # internally as UCS4. Note that UCS2 and UCS4 Python builds are not binary
    # compatible.
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    variant('dbm', default=True, description='Provide support for dbm')
    variant(
        'optimizations',
        default=False,
        description='Enable expensive build-time optimizations, if available'
    )
    # See https://legacy.python.org/dev/peps/pep-0394/
    variant('pythoncmd', default=True,
            description="Symlink 'python3' executable to 'python' "
            "(not PEP 394 compliant)")

    depends_on("openssl")
    depends_on("bzip2")
    depends_on("readline")
    depends_on("ncurses")
    depends_on("sqlite")
    depends_on("zlib")
    depends_on("tk", when="+tk")
    depends_on("tcl", when="+tk")
    depends_on("gdbm", when='+dbm')

    # Patch does not work for Python 3.1
    patch('ncurses.patch', when='@:2.8,3.2:')

    # Ensure that distutils chooses correct compiler option for RPATH on cray:
    patch('cray-rpath-2.3.patch', when="@2.3:3.0.1 platform=cray")
    patch('cray-rpath-3.1.patch', when="@3.1:3.99  platform=cray")

    # Fixes an alignment problem with more aggressive optimization in gcc8
    # https://github.com/python/cpython/commit/0b91f8a668201fc58fa732b8acc496caedfdbae0
    patch('gcc-8-2.7.14.patch', when="@2.7.14 %gcc@8:")

    # For more information refer to this bug report:
    # https://bugs.python.org/issue29712
    conflicts(
        '@:2.8 +shared',
        when='+optimizations',
        msg='+optimizations is incompatible with +shared in python@2.X'
    )

    _DISTUTIL_VARS_TO_SAVE = ['LDSHARED']
    _DISTUTIL_CACHE_FILENAME = 'sysconfig.json'
    _distutil_vars = None

    # An in-source build with --enable-optimizations fails for python@3.X
    build_directory = 'spack-build'

    @when('@2.7:2.8,3.4:')
    def patch(self):
        # NOTE: Python's default installation procedure makes it possible for a
        # user's local configurations to change the Spack installation.  In
        # order to prevent this behavior for a full installation, we must
        # modify the installation script so that it ignores user files.
        ff = FileFilter('Makefile.pre.in')
        ff.filter(
            r'^(.*)setup\.py(.*)((build)|(install))(.*)$',
            r'\1setup.py\2 --no-user-cfg \3\6'
        )

    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        # TODO: The '--no-user-cfg' option for Python installation is only in
        # Python v2.7 and v3.4+ (see https://bugs.python.org/issue1180) and
        # adding support for ignoring user configuration will require
        # significant changes to this package for other Python versions.
        if not spec.satisfies('@2.7,3.4:'):
            tty.warn(('Python v{0} may not install properly if Python '
                      'user configurations are present.').format(self.version))

        # Need this to allow python build to find the Python installation.
        spack_env.set('MACOSX_DEPLOYMENT_TARGET', platform.mac_ver()[0])

    def configure_args(self):
        spec = self.spec

        # setup.py needs to be able to read the CPPFLAGS and LDFLAGS
        # as it scans for the library and headers to build
        dep_pfxs = [dspec.prefix for dspec in spec.dependencies('link')]
        config_args = [
            '--with-threads',
            'CPPFLAGS=-I{0}'.format(' -I'.join(dp.include for dp in dep_pfxs)),
            'LDFLAGS=-L{0}'.format(' -L'.join(dp.lib for dp in dep_pfxs)),
        ]

        if spec.satisfies('@2.7.13:2.8,3.5.3:', strict=True) \
                and '+optimizations' in spec:
            config_args.append('--enable-optimizations')

        if spec.satisfies('%gcc platform=darwin'):
            config_args.append('--disable-toolbox-glue')

        if spec.satisfies('%intel', strict=True) and \
                spec.satisfies('@2.7.12:2.8,3.5.2:', strict=True):
            config_args.append('--with-icc')

        if '+shared' in spec:
            config_args.append('--enable-shared')
        else:
            config_args.append('--disable-shared')

        if '+ucs4' in spec:
            if spec.satisfies('@:2.7'):
                config_args.append('--enable-unicode=ucs4')
            elif spec.satisfies('@3.0:3.2'):
                config_args.append('--with-wide-unicode')
            elif spec.satisfies('@3.3:'):
                # https://docs.python.org/3.3/whatsnew/3.3.html
                raise ValueError(
                    '+ucs4 variant not compatible with Python 3.3 and beyond')

        if spec.satisfies('@3:'):
            config_args.append('--without-ensurepip')

        if '+pic' in spec:
            config_args.append('CFLAGS={0}'.format(self.compiler.pic_flag))

        return config_args

    @run_after('install')
    def post_install(self):
        spec = self.spec
        prefix = self.prefix

        self.sysconfigfilename = '_sysconfigdata.py'
        if spec.satisfies('@3.6:'):
            # Python 3.6.0 renamed the sys config file
            sc = 'import sysconfig; print(sysconfig._get_sysconfigdata_name())'
            cf = self.command('-c', sc, output=str).strip()
            self.sysconfigfilename = '{0}.py'.format(cf)

        self._save_distutil_vars(prefix)

        self.filter_compilers(prefix)

        # TODO:
        # On OpenSuse 13, python uses <prefix>/lib64/python2.7/lib-dynload/*.so
        # instead of <prefix>/lib/python2.7/lib-dynload/*.so. Oddly enough the
        # result is that Python can not find modules like cPickle. A workaround
        # for now is to symlink to `lib`:
        src = os.path.join(prefix.lib64,
                           'python{0}'.format(self.version.up_to(2)),
                           'lib-dynload')
        dst = os.path.join(prefix.lib,
                           'python{0}'.format(self.version.up_to(2)),
                           'lib-dynload')
        if os.path.isdir(src) and not os.path.isdir(dst):
            mkdirp(dst)
            for f in os.listdir(src):
                os.symlink(os.path.join(src, f),
                           os.path.join(dst, f))

        if spec.satisfies('@3:') and spec.satisfies('+pythoncmd'):
            os.symlink(os.path.join(prefix.bin, 'python3'),
                       os.path.join(prefix.bin, 'python'))
            os.symlink(os.path.join(prefix.bin, 'python3-config'),
                       os.path.join(prefix.bin, 'python-config'))

    # TODO: Once better testing support is integrated, add the following tests
    # https://wiki.python.org/moin/TkInter
    #
    # Note: Only works if ForwardX11Trusted is enabled, i.e. `ssh -Y`
    #
    #    if '+tk' in spec:
    #        env['TK_LIBRARY']  = join_path(spec['tk'].prefix.lib,
    #            'tk{0}'.format(spec['tk'].version.up_to(2)))
    #        env['TCL_LIBRARY'] = join_path(spec['tcl'].prefix.lib,
    #            'tcl{0}'.format(spec['tcl'].version.up_to(2)))
    #
    #        $ python
    #        >>> import _tkinter
    #
    #        if spec.satisfies('@3:')
    #            >>> import tkinter
    #            >>> tkinter._test()
    #        else:
    #            >>> import Tkinter
    #            >>> Tkinter._test()

    def _save_distutil_vars(self, prefix):
        """
        Run before changing automatically generated contents of the
        _sysconfigdata.py, which is used by distutils to figure out what
        executables to use while compiling and linking extensions. If we build
        extensions with spack those executables should be spack's wrappers.
        Spack partially covers this by setting environment variables that
        are also accounted for by distutils. Currently there is one more known
        variable that must be set, which is LDSHARED, so the method saves its
        autogenerated value to pass it to the dependent package's setup script.
        """

        self._distutil_vars = {}

        input_filename = None
        for filename in [join_path(lib_dir,
                                   'python{0}'.format(self.version.up_to(2)),
                                   self.sysconfigfilename)
                         for lib_dir in [prefix.lib, prefix.lib64]]:
            if os.path.isfile(filename):
                input_filename = filename
                break
        if not input_filename:
            return

        input_dict = None
        try:
            with open(input_filename) as input_file:
                match = re.search(r'build_time_vars\s*=\s*(?P<dict>{.*})',
                                  input_file.read(),
                                  flags=re.DOTALL)

                if match:
                    input_dict = ast.literal_eval(match.group('dict'))
        except (IOError, SyntaxError):
            pass

        if not input_dict:
            tty.warn("Failed to find 'build_time_vars' dictionary in file "
                     "'%s'. This might cause the extensions that are "
                     "installed with distutils to call compilers directly "
                     "avoiding Spack's wrappers." % input_filename)
            return

        for var_name in Python._DISTUTIL_VARS_TO_SAVE:
            if var_name in input_dict:
                self._distutil_vars[var_name] = input_dict[var_name]
            else:
                tty.warn("Failed to find key '%s' in 'build_time_vars' "
                         "dictionary in file '%s'. This might cause the "
                         "extensions that are installed with distutils to "
                         "call compilers directly avoiding Spack's wrappers."
                         % (var_name, input_filename))

        if len(self._distutil_vars) > 0:
            output_filename = None
            try:
                output_filename = join_path(
                    spack.store.layout.metadata_path(self.spec),
                    Python._DISTUTIL_CACHE_FILENAME)
                with open(output_filename, 'w') as output_file:
                    sjson.dump(self._distutil_vars, output_file)
            except Exception:
                tty.warn("Failed to save metadata for distutils. This might "
                         "cause the extensions that are installed with "
                         "distutils to call compilers directly avoiding "
                         "Spack's wrappers.")
                # We make the cache empty if we failed to save it to file
                # to provide the same behaviour as in the case when the cache
                # is initialized by the method load_distutils_data().
                self._distutil_vars = {}
                if output_filename:
                    force_remove(output_filename)

    def _load_distutil_vars(self):
        # We update and keep the cache unchanged only if the package is
        # installed.
        if not self._distutil_vars and self.installed:
            try:
                input_filename = join_path(
                    spack.store.layout.metadata_path(self.spec),
                    Python._DISTUTIL_CACHE_FILENAME)
                if os.path.isfile(input_filename):
                    with open(input_filename) as input_file:
                        self._distutil_vars = sjson.load(input_file)
            except Exception:
                pass

            if not self._distutil_vars:
                self._distutil_vars = {}

        return self._distutil_vars

    def filter_compilers(self, prefix):
        """Run after install to tell the configuration files and Makefiles
        to use the compilers that Spack built the package with.

        If this isn't done, they'll have CC and CXX set to Spack's generic
        cc and c++. We want them to be bound to whatever compiler
        they were built with."""

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}

        lib_dirnames = [
            join_path(lib_dir, 'python{0}'.format(self.version.up_to(2))) for
            lib_dir in [prefix.lib, prefix.lib64]]

        config_dirname = 'config-{0}m'.format(
            self.version.up_to(2)) if self.spec.satisfies('@3:') else 'config'

        rel_filenames = [self.sysconfigfilename,
                         join_path(config_dirname, 'Makefile')]

        abs_filenames = [join_path(dirname, filename) for dirname in
                         lib_dirnames for filename in rel_filenames]

        filter_file(env['CC'], self.compiler.cc, *abs_filenames, **kwargs)
        filter_file(env['CXX'], self.compiler.cxx, *abs_filenames, **kwargs)

    # ========================================================================
    # Set up environment to make install easy for python extensions.
    # ========================================================================

    @property
    def command(self):
        """Returns the Python command, which may vary depending
        on the version of Python and how it was installed.

        In general, Python 2 comes with ``python`` and ``python2`` commands,
        while Python 3 only comes with a ``python3`` command.

        :returns: The Python command
        :rtype: Executable
        """
        # We need to be careful here. If the user is using an externally
        # installed python, all 3 commands could be in the same directory.

        # Search for `python2` iff using Python 2
        if (self.spec.satisfies('@:2') and
                os.path.exists(os.path.join(self.prefix.bin, 'python2'))):
            command = 'python2'
        # Search for `python3` iff using Python 3
        elif (self.spec.satisfies('@3:') and
                os.path.exists(os.path.join(self.prefix.bin, 'python3'))):
            command = 'python3'
        # If neither were found, try `python`
        elif os.path.exists(os.path.join(self.prefix.bin, 'python')):
            command = 'python'
        else:
            msg = 'Unable to locate {0} command in {1}'
            raise RuntimeError(msg.format(self.name, self.prefix.bin))

        # The python command may be a symlink if it was installed
        # with Homebrew. Since some packages try to determine the
        # location of libraries and headers based on the path,
        # return the realpath
        path = os.path.realpath(os.path.join(self.prefix.bin, command))

        return Executable(path)

    def print_string(self, string):
        """Returns the appropriate print string depending on the
        version of Python.

        Examples:

        * Python 2

          .. code-block:: python

             >>> self.print_string('sys.prefix')
             'print sys.prefix'

        * Python 3

          .. code-block:: python

             >>> self.print_string('sys.prefix')
             'print(sys.prefix)'
        """
        if self.spec.satisfies('@:2'):
            return 'print {0}'.format(string)
        else:
            return 'print({0})'.format(string)

    def get_config_var(self, key):
        """Returns the value of a single variable. Wrapper around
        ``distutils.sysconfig.get_config_var()``."""

        cmd = 'from distutils.sysconfig import get_config_var; '
        cmd += self.print_string("get_config_var('{0}')".format(key))

        return self.command('-c', cmd, output=str).strip()

    def get_config_h_filename(self):
        """Returns the full path name of the configuration header.
        Wrapper around ``distutils.sysconfig.get_config_h_filename()``."""

        cmd = 'from distutils.sysconfig import get_config_h_filename; '
        cmd += self.print_string('get_config_h_filename()')

        return self.command('-c', cmd, output=str).strip()

    @property
    def home(self):
        """Most of the time, ``PYTHONHOME`` is simply
        ``spec['python'].prefix``. However, if the user is using an
        externally installed python, it may be symlinked. For example,
        Homebrew installs python in ``/usr/local/Cellar/python/2.7.12_2``
        and symlinks it to ``/usr/local``. Users may not know the actual
        installation directory and add ``/usr/local`` to their
        ``packages.yaml`` unknowingly. Query the python executable to
        determine exactly where it is installed."""

        prefix = self.get_config_var('prefix')
        return Prefix(prefix)

    @property
    def libs(self):
        # Spack installs libraries into lib, except on openSUSE where it
        # installs them into lib64. If the user is using an externally
        # installed package, it may be in either lib or lib64, so we need
        # to ask Python where its LIBDIR is.
        libdir = self.get_config_var('LIBDIR')

        # The system Python installation on macOS and Homebrew installations
        # install libraries into a Frameworks directory
        frameworkprefix = self.get_config_var('PYTHONFRAMEWORKPREFIX')

        if '+shared' in self.spec:
            ldlibrary = self.get_config_var('LDLIBRARY')

            if os.path.exists(os.path.join(libdir, ldlibrary)):
                return LibraryList(os.path.join(libdir, ldlibrary))
            elif os.path.exists(os.path.join(frameworkprefix, ldlibrary)):
                return LibraryList(os.path.join(frameworkprefix, ldlibrary))
            else:
                msg = 'Unable to locate {0} libraries in {1}'
                raise RuntimeError(msg.format(self.name, libdir))
        else:
            library = self.get_config_var('LIBRARY')

            if os.path.exists(os.path.join(libdir, library)):
                return LibraryList(os.path.join(libdir, library))
            elif os.path.exists(os.path.join(frameworkprefix, library)):
                return LibraryList(os.path.join(frameworkprefix, library))
            else:
                msg = 'Unable to locate {0} libraries in {1}'
                raise RuntimeError(msg.format(self.name, libdir))

    @property
    def headers(self):
        config_h = self.get_config_h_filename()

        if os.path.exists(config_h):
            return HeaderList(config_h)
        else:
            includepy = self.get_config_var('INCLUDEPY')
            msg = 'Unable to locate {0} headers in {1}'
            raise RuntimeError(msg.format(self.name, includepy))

    @property
    def python_lib_dir(self):
        return join_path('lib', 'python{0}'.format(self.version.up_to(2)))

    @property
    def python_include_dir(self):
        return join_path('include', 'python{0}'.format(self.version.up_to(2)))

    @property
    def site_packages_dir(self):
        return join_path(self.python_lib_dir, 'site-packages')

    @property
    def easy_install_file(self):
        return join_path(self.site_packages_dir, "easy-install.pth")

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Set PYTHONPATH to include the site-packages directory for the
        extension and any other python extensions it depends on."""

        # If we set PYTHONHOME, we must also ensure that the corresponding
        # python is found in the build environment. This to prevent cases
        # where a system provided python is run against the standard libraries
        # of a Spack built python. See issue #7128
        spack_env.set('PYTHONHOME', self.home)

        path = os.path.dirname(self.command.path)
        if not is_system_path(path):
            spack_env.prepend_path('PATH', path)

        python_paths = []
        for d in dependent_spec.traverse(
                deptype=('build', 'run', 'test')):
            if d.package.extends(self.spec):
                python_paths.append(join_path(d.prefix,
                                              self.site_packages_dir))

        pythonpath = ':'.join(python_paths)
        spack_env.set('PYTHONPATH', pythonpath)

        # For run time environment set only the path for
        # dependent_spec and prepend it to PYTHONPATH
        if dependent_spec.package.extends(self.spec):
            run_env.prepend_path('PYTHONPATH', join_path(
                dependent_spec.prefix, self.site_packages_dir))

    def setup_dependent_package(self, module, dependent_spec):
        """Called before python modules' install() methods.

        In most cases, extensions will only need to have one line::

        setup_py('install', '--prefix={0}'.format(prefix))"""

        module.python = self.command
        module.setup_py = Executable(
            self.command.path + ' setup.py --no-user-cfg')

        distutil_vars = self._load_distutil_vars()

        if distutil_vars:
            for key, value in distutil_vars.items():
                module.setup_py.add_default_env(key, value)

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir = join_path(dependent_spec.prefix,
                                          self.python_lib_dir)
        module.python_include_dir = join_path(dependent_spec.prefix,
                                              self.python_include_dir)
        module.site_packages_dir = join_path(dependent_spec.prefix,
                                             self.site_packages_dir)

        self.spec.home = self.home

        # Make the site packages directory for extensions
        if dependent_spec.package.is_extension:
            mkdirp(module.site_packages_dir)

    # ========================================================================
    # Handle specifics of activating and deactivating python modules.
    # ========================================================================

    def python_ignore(self, ext_pkg, args):
        """Add some ignore files to activate/deactivate args."""
        ignore_arg = args.get('ignore', lambda f: False)

        # Always ignore easy-install.pth, as it needs to be merged.
        patterns = [r'site-packages/easy-install\.pth$']

        # Ignore pieces of setuptools installed by other packages.
        # Must include directory name or it will remove all site*.py files.
        if ext_pkg.name != 'py-setuptools':
            patterns.extend([
                r'bin/easy_install[^/]*$',
                r'site-packages/setuptools[^/]*\.egg$',
                r'site-packages/setuptools\.pth$',
                r'site-packages/site[^/]*\.pyc?$',
                r'site-packages/__pycache__/site[^/]*\.pyc?$'
            ])
        if ext_pkg.name != 'py-pygments':
            patterns.append(r'bin/pygmentize$')
        if ext_pkg.name != 'py-numpy':
            patterns.append(r'bin/f2py[0-9.]*$')

        return match_predicate(ignore_arg, patterns)

    def write_easy_install_pth(self, exts, prefix=None):
        if not prefix:
            prefix = self.prefix

        paths = []
        unique_paths = set()

        for ext in sorted(exts.values()):
            easy_pth = join_path(ext.prefix, self.easy_install_file)

            if not os.path.isfile(easy_pth):
                continue

            with open(easy_pth) as f:
                for line in f:
                    line = line.rstrip()

                    # Skip lines matching these criteria
                    if not line:
                        continue
                    if re.search(r'^(import|#)', line):
                        continue
                    if (ext.name != 'py-setuptools' and
                            re.search(r'setuptools.*egg$', line)):
                        continue

                    if line not in unique_paths:
                        unique_paths.add(line)
                        paths.append(line)

        main_pth = join_path(prefix, self.easy_install_file)

        if not paths:
            if os.path.isfile(main_pth):
                os.remove(main_pth)

        else:
            with open(main_pth, 'w') as f:
                f.write("import sys; sys.__plen = len(sys.path)\n")
                for path in paths:
                    f.write("{0}\n".format(path))
                f.write("import sys; new=sys.path[sys.__plen:]; "
                        "del sys.path[sys.__plen:]; "
                        "p=getattr(sys,'__egginsert',0); "
                        "sys.path[p:p]=new; "
                        "sys.__egginsert = p+len(new)\n")

    def activate(self, ext_pkg, view, **args):
        ignore = self.python_ignore(ext_pkg, args)
        args.update(ignore=ignore)

        super(Python, self).activate(ext_pkg, view, **args)

        extensions_layout = view.extensions_layout
        exts = extensions_layout.extension_map(self.spec)
        exts[ext_pkg.name] = ext_pkg.spec

        self.write_easy_install_pth(exts, prefix=view.root)

    def deactivate(self, ext_pkg, view, **args):
        args.update(ignore=self.python_ignore(ext_pkg, args))

        super(Python, self).deactivate(ext_pkg, view, **args)

        extensions_layout = view.extensions_layout
        exts = extensions_layout.extension_map(self.spec)
        # Make deactivate idempotent
        if ext_pkg.name in exts:
            del exts[ext_pkg.name]
            self.write_easy_install_pth(exts, prefix=view.root)

    def add_files_to_view(self, view, merge_map):
        bin_dir = self.spec.prefix.bin
        for src, dst in merge_map.items():
            if not path_contains_subdirectory(src, bin_dir):
                view.link(src, dst)
            elif not os.path.islink(src):
                copy(src, dst)
                if 'script' in get_filetype(src):
                    filter_file(
                        self.spec.prefix, os.path.abspath(view.root), dst)
            else:
                orig_link_target = os.path.realpath(src)
                new_link_target = os.path.abspath(merge_map[orig_link_target])
                view.link(new_link_target, dst)

    def remove_files_from_view(self, view, merge_map):
        bin_dir = self.spec.prefix.bin
        for src, dst in merge_map.items():
            if not path_contains_subdirectory(src, bin_dir):
                view.remove_file(src, dst)
            else:
                os.remove(dst)
