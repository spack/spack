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


class PyShiboken(PythonPackage):
    """Shiboken generates bindings for C++ libraries using CPython."""
    homepage = "https://shiboken.readthedocs.org/"
    url      = "https://pypi.python.org/packages/source/S/Shiboken/Shiboken-1.2.2.tar.gz"

    version('1.2.2', '345cfebda221f525842e079a6141e555')

    depends_on('cmake', type='build')

    depends_on("py-setuptools", type='build')
    depends_on("py-sphinx", type=('build', 'run'))
    depends_on("libxml2")
    depends_on("qt@:4.8")

    def patch(self):
        """Undo Shiboken RPATH handling and add Spack RPATH."""
        # Add Spack's standard CMake args to the sub-builds.
        # They're called BY setup.py so we have to patch it.
        pypkg = self.spec['python'].package
        rpath = self.rpath
        rpath.append(os.path.join(
            self.prefix, pypkg.site_packages_dir, 'Shiboken'))

        filter_file(
            r'OPTION_CMAKE,',
            r'OPTION_CMAKE, ' + (
                '"-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE", '
                '"-DCMAKE_INSTALL_RPATH=%s",' % ':'.join(rpath)),
            'setup.py')

        # Shiboken tries to patch ELF files to remove RPATHs
        # Disable this and go with the one we set.
        filter_file(
            r'^\s*rpath_cmd\(shiboken_path, srcpath\)',
            r'#rpath_cmd(shiboken_path, srcpath)',
            'shiboken_postinstall.py')

    def build_args(self, spec, prefix):
        return ['--jobs={0}'.format(make_jobs)]
