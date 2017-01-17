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
from spack import *
import os


class PyPyside(PythonPackage):
    """Python bindings for Qt."""
    homepage = "https://pypi.python.org/pypi/pyside"
    url      = "https://pypi.python.org/packages/source/P/PySide/PySide-1.2.2.tar.gz"

    version('1.2.4', '3cb7174c13bd45e3e8f77638926cb8c0')  # rpath problems
    version('1.2.2', 'c45bc400c8a86d6b35f34c29e379e44d', preferred=True)

    depends_on('cmake', type='build')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx', type=('build', 'run'))
    depends_on('qt@4.5:4.9')
    depends_on('libxml2@2.6.32:')
    depends_on('libxslt@1.1.19:')

    def patch(self):
        """Undo PySide RPATH handling and add Spack RPATH."""
        # Figure out the special RPATH
        pypkg = self.spec['python'].package
        rpath = self.rpath
        rpath.append(os.path.join(
            self.prefix, pypkg.site_packages_dir, 'PySide'))

        # Add Spack's standard CMake args to the sub-builds.
        # They're called BY setup.py so we have to patch it.
        filter_file(
            r'OPTION_CMAKE,',
            r'OPTION_CMAKE, ' + (
                '"-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE", '
                '"-DCMAKE_INSTALL_RPATH=%s",' % ':'.join(rpath)),
            'setup.py')

        # PySide tries to patch ELF files to remove RPATHs
        # Disable this and go with the one we set.
        if self.spec.satisfies('@1.2.4:'):
            rpath_file = 'setup.py'
        else:
            rpath_file = 'pyside_postinstall.py'

        filter_file(r'(^\s*)(rpath_cmd\(.*\))', r'\1#\2', rpath_file)

        # TODO: rpath handling for PySide 1.2.4 still doesn't work.
        # PySide can't find the Shiboken library, even though it comes
        # bundled with it and is installed in the same directory.

        # PySide does not provide official support for
        # Python 3.5, but it should work fine
        filter_file("'Programming Language :: Python :: 3.4'",
                    "'Programming Language :: Python :: 3.4',\r\n        "
                    "'Programming Language :: Python :: 3.5'",
                    "setup.py")

    def build_args(self, spec, prefix):
        return ['--jobs={0}'.format(make_jobs)]
