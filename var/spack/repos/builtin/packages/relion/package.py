##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Relion(CMakePackage):
    """RELION (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a
    stand-alone computer program that employs an empirical Bayesian approach to
    refinement of (multiple) 3D reconstructions or 2D class averages in
    electron cryo-microscopy (cryo-EM)."""

    homepage = "http://http://www2.mrc-lmb.cam.ac.uk/relion"
    url      = "https://github.com/3dem/relion/archive/2.0.3.tar.gz"

    version('2.0.3', 'c61be5ef00848806278b341f43893f5d')

    variant('gui', default=True, description="build the gui")
    variant('cuda', default=False, description="enable compute on gpu")
    variant('double', default=False, description="double precision (cpu) code")
    variant('double-gpu', default=False, description="double precision (gpu) code")
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'Profiling', 'Benchmarking'))

    depends_on('mpi')
    depends_on('fftw+float+double')
    depends_on('fltk', when='+gui')
    depends_on('cuda', when='+cuda')

    def cmake_args(self):
        args = [
            '-DCMAKE_C_FLAGS=-g',
            '-DCMAKE_CXX_FLAGS=-g',
            '-DGUI=%s' % ('+gui' in self.spec),
            '-DDoublePrec_CPU=%s' % ('+double' in self.spec),
            '-DDoublePrec_GPU=%s' % ('+double-gpu' in self.spec),
        ]
        if '+cuda' in self.spec:
            args += [
                '-DCUDA=on',
                '-DCUFFT=on',
            ]
        return args
