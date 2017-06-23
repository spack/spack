##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from spack import *


class PyBasemap(PythonPackage):
    """The matplotlib basemap toolkit is a library for plotting
    2D data on maps in Python."""

    homepage = "http://matplotlib.org/basemap/"
    url      = "https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz"

    version('1.0.7', '48c0557ced9e2c6e440b28b3caff2de8')

    # Per Github issue #3813, setuptools is required at runtime in order
    # to make mpl_toolkits a namespace package that can span multiple
    # directories (i.e., matplotlib and basemap)
    depends_on('py-setuptools', type='run')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('geos')

    def install(self, spec, prefix):
        # The default `install` method adds `--single-version-external-managed`
        # because the package depends on py-setuptools. But the package doesn't
        # actually build with `py-setuptools`, it just needs it at run-time.
        # Until I can figure out how to query direct build dependencies only,
        # override the default `install` method.
        args = self.install_args(spec, prefix)

        args.append('--prefix={0}'.format(prefix))

        self.setup_py('install', *args)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GEOS_DIR', self.spec['geos'].prefix)
