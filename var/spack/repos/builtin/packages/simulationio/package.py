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


class Simulationio(CMakePackage):
    """SimulationIO: Efficient and convenient I/O for large PDE simulations"""
    homepage = "https://github.com/eschnett/SimulationIO"
    url= "https://github.com/eschnett/SimulationIO/archive/version/0.1.0.tar.gz"

    version('1.0.0', '5cbf1d0084eb436d861ffcdd297eaa08')
    version('0.1.0', '00f7dabc08ed1ab77858785ce0809f50')
    version('develop',
            git='https://github.com/eschnett/SimulationIO.git', branch='master')

    variant('julia', default=False)
    variant('python', default=True)

    variant('pic', default=True,
            description="Produce position-independent code")

    depends_on('julia', when='+julia', type=('build', 'run'))
    depends_on('py-h5py', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('python@2.7.0:2.999.999', when='+python', type=('build', 'run'))
    depends_on('swig', type='build')

    extends('python')

    def cmake_args(self):
        spec = self.spec
        options = []
        if '+pic' in spec:
            options.append("-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true")
        return options

    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAILURE=1")
