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
import os
import re
from contextlib import closing

import spack
from llnl.util.lang import match_predicate
from spack import *
from spack.util.environment import *


class Python(Package):
    """The Python programming language."""

    homepage = "http://www.python.org"
    url      = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz"

    version('3.5.1', 'be78e48cdfc1a7ad90efff146dce6cfe')
    version('3.5.0', 'a56c0c0b45d75a0ec9c6dee933c41c36')
    version('2.7.11', '6b6076ec9e93f05dd63e47eb9c15728b', preferred=True)
    version('2.7.10', 'd7547558fd673bd9d38e2108c6b42521')
    version('2.7.9', '5eebcaa0030dc4061156d3429657fb83')
    version('2.7.8', 'd4bca0159acb0b44a781292b5231936f')

    extendable = True

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

        # Rest of install is pretty standard except setup.py needs to
        # be able to read the CPPFLAGS and LDFLAGS as it scans for the
        # library and headers to build
        cppflags = ' -I'.join([
            spec['openssl'].prefix.include,  spec['bzip2'].prefix.include,
            spec['readline'].prefix.include, spec['ncurses'].prefix.include,
            spec['sqlite'].prefix.include,   spec['zlib'].prefix.include
        ])

        ldflags = ' -L'.join([
            spec['openssl'].prefix.lib,  spec['bzip2'].prefix.lib,
            spec['readline'].prefix.lib, spec['ncurses'].prefix.lib,
            spec['sqlite'].prefix.lib,   spec['zlib'].prefix.lib
        ])

        config_args = [
            "--prefix={0}".format(prefix),
            "--with-threads",
            "--enable-shared",
            "CPPFLAGS=-I{0}".format(cppflags),
            "LDFLAGS=-L{0}".format(ldflags)
        ]

        if spec.satisfies('@3:'):
            config_args.append('--without-ensurepip')

        configure(*config_args)

        make()
        make("install")

        self.filter_compilers(spec, prefix)

    def filter_compilers(self, spec, prefix):
        """Run after install to tell the configuration files and Makefiles
        to use the compilers that Spack built the package with.

        If this isn't done, they'll have CC and CXX set to Spack's generic
        cc and c++. We want them to be bound to whatever compiler
        they were built with."""

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}

        dirname = join_path(prefix.lib,
                            'python{0}'.format(self.version.up_to(2)))

        config = 'config'
        if spec.satisfies('@3:'):
            config = 'config-{0}m'.format(self.version.up_to(2))

        files = [
            '_sysconfigdata.py',
            join_path(config, 'Makefile')
        ]

        for filename in files:
            filter_file(env['CC'],  self.compiler.cc,
                        join_path(dirname, filename), **kwargs)
            filter_file(env['CXX'], self.compiler.cxx,
                        join_path(dirname, filename), **kwargs)

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

        python_paths = []
        for d in extension_spec.traverse():
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

        python('setup.py', 'install', '--prefix={0}'.format(prefix))"""

        # Python extension builds can have a global python executable function
        if Version("3.0.0") <= self.version < Version("4.0.0"):
            module.python = Executable(join_path(self.spec.prefix.bin,
                                                 'python3'))
        else:
            module.python = Executable(join_path(self.spec.prefix.bin,
                                                 'python'))

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir     = join_path(ext_spec.prefix,
                                              self.python_lib_dir)
        module.python_include_dir = join_path(ext_spec.prefix,
                                              self.python_include_dir)
        module.site_packages_dir  = join_path(ext_spec.prefix,
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
            patterns.append(r'bin/f2py$')
            patterns.append(r'bin/f2py3$')

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
                    if ((ext.name != 'py-setuptools' and
                         re.search(r'setuptools.*egg$', line))):
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

        exts = spack.install_layout.extension_map(self.spec)
        exts[ext_pkg.name] = ext_pkg.spec
        self.write_easy_install_pth(exts)

    def deactivate(self, ext_pkg, **args):
        args.update(ignore=self.python_ignore(ext_pkg, args))
        super(Python, self).deactivate(ext_pkg, **args)

        exts = spack.install_layout.extension_map(self.spec)
        # Make deactivate idempotent
        if ext_pkg.name in exts:
            del exts[ext_pkg.name]
            self.write_easy_install_pth(exts)
