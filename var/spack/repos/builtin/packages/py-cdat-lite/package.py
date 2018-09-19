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
#
from spack import *


class PyCdatLite(PythonPackage):
    """Cdat-lite is a Python package for managing and analysing climate
    science data. It is a subset of the Climate Data Analysis Tools (CDAT)
    developed by PCMDI at Lawrence Livermore National Laboratory."""

    homepage = "http://proj.badc.rl.ac.uk/cedaservices/wiki/CdatLite"
    url      = "https://pypi.io/packages/source/c/cdat-lite/cdat-lite-6.0.1.tar.gz"

    version('6.0.1', '6d5a6e86f15ce15291d25feab8793248')

    depends_on("netcdf")
    depends_on("python@2.5:2.8", type=('build', 'run'))
    depends_on("py-numpy", type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    phases = ['install']

    def install(self, spec, prefix):
        """Install everything from build directory."""
        install_args = self.install_args(spec, prefix)
        # Combine all phases into a single setup.py command,
        # otherwise extensions are rebuilt without rpath by install phase:
        self.setup_py('build_ext', '--rpath=%s' % ":".join(self.rpath),
                      'build_py', 'build_scripts',
                      'install', *install_args)
