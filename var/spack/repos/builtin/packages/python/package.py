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
import functools
import glob
import inspect
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

    extendable = True

    version('3.5.1', 'be78e48cdfc1a7ad90efff146dce6cfe')
    version('3.5.0', 'a56c0c0b45d75a0ec9c6dee933c41c36')
    version('2.7.11', '6b6076ec9e93f05dd63e47eb9c15728b', preferred=True)
    version('2.7.10', 'd7547558fd673bd9d38e2108c6b42521')
    version('2.7.9', '5eebcaa0030dc4061156d3429657fb83')
    version('2.7.8', 'd4bca0159acb0b44a781292b5231936f')

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

        # Modify compiler paths in configuration files. This is necessary for
        # building site packages outside of spack
        filter_file(r'([/s]=?)([\S=]*)/lib/spack/env(/[^\s/]*)?/(\S*)(\s)',
                    (r'\4\5'),
                    join_path(prefix.lib, 'python%d.%d' % self.version[:2], '_sysconfigdata.py'))

        python3_version = ''
        if spec.satisfies('@3:'):
            python3_version = '-%d.%dm' % self.version[:2]
        makefile_filepath = join_path(prefix.lib, 'python%d.%d' % self.version[:2], 'config%s' % python3_version, 'Makefile')
        filter_file(r'([/s]=?)([\S=]*)/lib/spack/env(/[^\s/]*)?/(\S*)(\s)',
                    (r'\4\5'),
                    makefile_filepath)


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


    def setup_dependent_environment(self, spack_env, run_env, extension_spec):
        # TODO: do this only for actual extensions.

        # Set PYTHONPATH to include site-packages dir for the
        # extension and any other python extensions it depends on.
        python_paths = []
        for d in extension_spec.traverse():
            if d.package.extends(self.spec):
                python_paths.append(os.path.join(d.prefix, self.site_packages_dir))

        pythonpath = ':'.join(python_paths)
        spack_env.set('PYTHONPATH', pythonpath)

        # For run time environment set only the path for extension_spec and prepend it to PYTHONPATH
        if extension_spec.package.extends(self.spec):
            run_env.prepend_path('PYTHONPATH', os.path.join(extension_spec.prefix, self.site_packages_dir))


    def setup_dependent_package(self, module, ext_spec):
        """
        Called before python modules' install() methods.

        In most cases, extensions will only need to have one line::

        python('setup.py', 'install', '--prefix=%s' % prefix)
        """
        # Python extension builds can have a global python executable function
        if self.version >= Version("3.0.0") and self.version < Version("4.0.0"):
            module.python = Executable(join_path(self.spec.prefix.bin, 'python3'))
        else:
            module.python = Executable(join_path(self.spec.prefix.bin, 'python'))

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir     = os.path.join(ext_spec.prefix, self.python_lib_dir)
        module.python_include_dir = os.path.join(ext_spec.prefix, self.python_include_dir)
        module.site_packages_dir  = os.path.join(ext_spec.prefix, self.site_packages_dir)

        # Make the site packages directory for extensions, if it does not exist already.
        if ext_spec.package.is_extension:
            mkdirp(module.site_packages_dir)

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
        if ext_pkg.name != 'py-numpy':
            patterns.append(r'bin/f2py$')

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
