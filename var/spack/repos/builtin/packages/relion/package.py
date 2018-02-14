##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
from spack import *


class Relion(CMakePackage):
    """RELION (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a
    stand-alone computer program that employs an empirical Bayesian approach to
    refinement of (multiple) 3D reconstructions or 2D class averages in
    electron cryo-microscopy (cryo-EM)."""

    homepage = "http://http://www2.mrc-lmb.cam.ac.uk/relion"
    url      = "https://github.com/3dem/relion"

    version('2.1', git='https://github.com/3dem/relion.git', tag='2.1')
    version('2.0.3', git='https://github.com/3dem/relion.git', tag='2.0.3')
    version('develop', git='https://github.com/3dem/relion.git')

    variant('gui', default=True, description="build the gui")
    variant('cuda', default=True, description="enable compute on gpu")
    variant('cuda_arch', default=None, description='CUDA architecture',
           values=('20', '30', '32', '35', '50', '52', '53', '60', '61', '62'
               '70'),
           multi=True)
    variant('double', default=True, description="double precision (cpu) code")
    variant('double-gpu', default=False, description="double precision (gpu) code")
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'Profiling', 'Benchmarking'))

    depends_on('mpi')
    depends_on('fftw+float+double')
    depends_on('fltk', when='+gui')
    # cuda 9 not yet supported
    #  https://github.com/3dem/relion/issues/296
    depends_on('cuda@8.0:8.99', when='+cuda')
    # use gcc < 5 when compiled with cuda 8
    conflicts('%gcc@5:', when='+cuda')

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
            ]

        carch = self.spec.variants['cuda_arch'].value

        if carch is not None:
            args += [
                '-DCUDA_ARCH=%s' % (carch),
            ]
        return args
