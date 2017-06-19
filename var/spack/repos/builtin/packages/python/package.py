##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import re
from contextlib import closing

import spack
import llnl.util.tty as tty
from llnl.util.lang import match_predicate
from llnl.util.filesystem import force_remove
from spack import *
from spack.util.environment import *
import spack.util.spack_json as sjson


class Python(Package):
    """The Python programming language."""

    homepage = "http://www.python.org"
    url = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz"
    list_url = "https://www.python.org/downloads/"
    list_depth = 2

    version('3.6.0', '3f7062ccf8be76491884d0e47ac8b251')
    version('3.5.2', '3fe8434643a78630c61c6464fe2e7e72')
    version('3.5.1', 'be78e48cdfc1a7ad90efff146dce6cfe')
    version('3.5.0', 'a56c0c0b45d75a0ec9c6dee933c41c36')
    version('3.4.3', '4281ff86778db65892c05151d5de738d')
    version('3.3.6', 'cdb3cd08f96f074b3f3994ccb51063e9')
    version('3.2.6', '23815d82ae706e9b781ca65865353d39')
    version('3.1.5', '02196d3fc7bc76bdda68aa36b0dd16ab')
    version('2.7.13', '17add4bf0ad0ec2f08e0cae6d205c700', preferred=True)
    version('2.7.12', '88d61f82e3616a4be952828b3694109d')
    version('2.7.11', '6b6076ec9e93f05dd63e47eb9c15728b')
    version('2.7.10', 'd7547558fd673bd9d38e2108c6b42521')
    version('2.7.9', '5eebcaa0030dc4061156d3429657fb83')
    version('2.7.8', 'd4bca0159acb0b44a781292b5231936f')

    extendable = True

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

    depends_on("openssl")
    depends_on("bzip2")
    depends_on("readline")
    depends_on("ncurses")
    depends_on("sqlite")
    depends_on("zlib")
    depends_on("tk", when="+tk")
    depends_on("tcl", when="+tk")

    patch('ncurses.patch')

    _DISTUTIL_VARS_TO_SAVE = ['LDSHARED']
    _DISTUTIL_CACHE_FILENAME = 'sysconfig.json'
    _distutil_vars = None

    @when('@2.7,3.4:')
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

    @when('@:2.6,3.0:3.3')
    def patch(self):
        # See https://github.com/LLNL/spack/issues/1490
        pass

    def install(self, spec, prefix):
        # TODO: The '--no-user-cfg' option for Python installation is only in
        # Python v2.7 and v3.4+ (see https://bugs.python.org/issue1180) and
        # adding support for ignoring user configuration will require
        # significant changes to this package for other Python versions.
        if not spec.satisfies('@2.7,3.4:'):
            tty.warn(('Python v{0} may not install properly if Python '
                      'user configurations are present.').format(self.version))

        # Need this to allow python build to find the Python installation.
        env['PYTHONHOME'], env['PYTHONPATH'] = prefix, prefix
        env['MACOSX_DEPLOYMENT_TARGET'] = '10.6'

        # Rest of install is pretty standard except setup.py needs to
        # be able to read the CPPFLAGS and LDFLAGS as it scans for the
        # library and headers to build
        dep_pfxs = [dspec.prefix for dspec in spec.dependencies('link')]
        config_args = [
            '--prefix={0}'.format(prefix),
            '--with-threads',
            '--enable-shared',
            'CPPFLAGS=-I{0}'.format(' -I'.join(dp.include for dp in dep_pfxs)),
            'LDFLAGS=-L{0}'.format(' -L'.join(dp.lib for dp in dep_pfxs)),
        ]
        if spec.satisfies("platform=darwin") and ('%gcc' in spec):
            config_args.append('--disable-toolbox-glue')

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

        configure(*config_args)
        make()
        make('install')

        self.sysconfigfilename = '_sysconfigdata.py'
        if spec.satisfies('@3.6:'):
            # Python 3.6.0 renamed the sys config file
            python3 = os.path.join(prefix.bin,
                                   'python{0}'.format(self.version.up_to(1)))
            python = Executable(python3)
            sc = 'import sysconfig; print(sysconfig._get_sysconfigdata_name())'
            cf = python('-c', sc, output=str).strip('\n')
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
        autogenerated value to pass it to the dependant package's setup script.
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
            tty.warn('Failed to find \'build_time_vars\' dictionary in file '
                     '\'%s\'. This might cause the extensions that are '
                     'installed with distutils to call compilers directly '
                     'avoiding Spack\'s wrappers.' % input_filename)
            return

        for var_name in Python._DISTUTIL_VARS_TO_SAVE:
            if var_name in input_dict:
                self._distutil_vars[var_name] = input_dict[var_name]
            else:
                tty.warn('Failed to find key \'%s\' in \'build_time_vars\' '
                         'dictionary in file \'%s\'. This might cause the '
                         'extensions that are installed with distutils to '
                         'call compilers directly avoiding Spack\'s wrappers.'
                         % (var_name, input_filename))

        if len(self._distutil_vars) > 0:
            output_filename = None
            try:
                output_filename = join_path(
                    spack.store.layout.metadata_path(self.spec),
                    Python._DISTUTIL_CACHE_FILENAME)
                with open(output_filename, 'w') as output_file:
                    sjson.dump(self._distutil_vars, output_file)
            except:
                tty.warn('Failed to save metadata for distutils. This might '
                         'cause the extensions that are installed with '
                         'distutils to call compilers directly avoiding '
                         'Spack\'s wrappers.')
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
            except:
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
    def python_lib_dir(self):
        return join_path('lib', 'python{0}'.format(self.version.up_to(2)))

    @property
    def python_include_dir(self):
        return join_path('include', 'python{0}'.format(self.version.up_to(2)))

    @property
    def site_packages_dir(self):
        return join_path(self.python_lib_dir, 'site-packages')

    def setup_dependent_environment(self, spack_env, run_env, extension_spec):
        """Set PYTHONPATH to include site-packages dir for the
        extension and any other python extensions it depends on."""
        # The python executable for version 3 may be python3 or python
        # See https://github.com/LLNL/spack/pull/2173#issuecomment-257170199
        pythonex = 'python{0}'.format('3' if self.spec.satisfies('@3') else '')
        if os.path.isdir(self.prefix.bin):
            base = self.prefix.bin
        else:
            base = self.prefix
        if not os.path.isfile(os.path.join(base, pythonex)):
            if self.spec.satisfies('@3'):
                python = Executable(os.path.join(base, 'python'))
                version = python('-c', 'import sys; print(sys.version)',
                                 output=str)
                if version.startswith('3'):
                    pythonex = 'python'
                else:
                    raise RuntimeError('Cannot locate python executable')
            else:
                raise RuntimeError('Cannot locate python executable')
        python = Executable(os.path.join(base, pythonex))
        prefix = python('-c', 'import sys; print(sys.prefix)', output=str)
        spack_env.set('PYTHONHOME', prefix.strip('\n'))

        python_paths = []
        for d in extension_spec.traverse(
                deptype=('build', 'run'), deptype_query='run'):
            if d.package.extends(self.spec):
                python_paths.append(join_path(d.prefix,
                                              self.site_packages_dir))

        pythonpath = ':'.join(python_paths)
        spack_env.set('PYTHONPATH', pythonpath)

        # For run time environment set only the path for
        # extension_spec and prepend it to PYTHONPATH
        if extension_spec.package.extends(self.spec):
            run_env.prepend_path('PYTHONPATH', join_path(
                extension_spec.prefix, self.site_packages_dir))

    def setup_dependent_package(self, module, ext_spec):
        """Called before python modules' install() methods.

        In most cases, extensions will only need to have one line::

        setup_py('install', '--prefix={0}'.format(prefix))"""
        python_path = join_path(
            self.spec.prefix.bin,
            'python{0}'.format('3' if self.spec.satisfies('@3') else '')
        )

        module.python = Executable(python_path)
        module.setup_py = Executable(python_path + ' setup.py --no-user-cfg')

        distutil_vars = self._load_distutil_vars()

        if distutil_vars:
            for key, value in distutil_vars.iteritems():
                module.setup_py.add_default_env(key, value)

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir = join_path(ext_spec.prefix,
                                          self.python_lib_dir)
        module.python_include_dir = join_path(ext_spec.prefix,
                                              self.python_include_dir)
        module.site_packages_dir = join_path(ext_spec.prefix,
                                             self.site_packages_dir)

        # Make the site packages directory for extensions
        if ext_spec.package.is_extension:
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
            patterns.append(r'bin/f2py3?$')

        return match_predicate(ignore_arg, patterns)

    def write_easy_install_pth(self, exts):
        paths = []
        for ext in sorted(exts.values()):
            ext_site_packages = join_path(ext.prefix, self.site_packages_dir)
            easy_pth = join_path(ext_site_packages, "easy-install.pth")

            if not os.path.isfile(easy_pth):
                continue

            with closing(open(easy_pth)) as f:
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

                    paths.append(line)

        site_packages = join_path(self.prefix, self.site_packages_dir)
        main_pth = join_path(site_packages, "easy-install.pth")

        if not paths:
            if os.path.isfile(main_pth):
                os.remove(main_pth)

        else:
            with closing(open(main_pth, 'w')) as f:
                f.write("""
import sys
sys.__plen = len(sys.path)
""")
                for path in paths:
                    f.write("{0}\n".format(path))
                f.write("""
new = sys.path[sys.__plen:]
del sys.path[sys.__plen:]
p = getattr(sys, '__egginsert', 0)
sys.path[p:p] = new
sys.__egginsert = p + len(new)
""")

    def activate(self, ext_pkg, **args):
        ignore = self.python_ignore(ext_pkg, args)
        args.update(ignore=ignore)

        super(Python, self).activate(ext_pkg, **args)

        exts = spack.store.layout.extension_map(self.spec)
        exts[ext_pkg.name] = ext_pkg.spec
        self.write_easy_install_pth(exts)

    def deactivate(self, ext_pkg, **args):
        args.update(ignore=self.python_ignore(ext_pkg, args))
        super(Python, self).deactivate(ext_pkg, **args)

        exts = spack.store.layout.extension_map(self.spec)
        # Make deactivate idempotent
        if ext_pkg.name in exts:
            del exts[ext_pkg.name]
            self.write_easy_install_pth(exts)
