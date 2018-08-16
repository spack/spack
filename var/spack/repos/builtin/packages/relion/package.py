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
from spack import *


class Relion(CMakePackage, CudaPackage):
    """RELION (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a
    stand-alone computer program that employs an empirical Bayesian approach to
    refinement of (multiple) 3D reconstructions or 2D class averages in
    electron cryo-microscopy (cryo-EM)."""

    homepage = "http://http://www2.mrc-lmb.cam.ac.uk/relion"
    git      = "https://github.com/3dem/relion.git"

    version('3.0_beta',
            git='https://bitbucket.org/scheres/relion-3.0_beta.git')
    version('2.1', preferred='true', tag='2.1')
    version('2.0.3', tag='2.0.3')
    # relion has no develop branch though pulling from master
    # should be considered the same as develop
    version('develop', branch='master')

    variant('gui', default=True, description="build the gui")
    variant('cuda', default=True, description="enable compute on gpu")
    variant('double', default=True, description="double precision (cpu) code")
    variant('double-gpu', default=False, description="double precision gpu")
    # if built with purpose=cluster then relion will link to gpfs libraries
    # if that's not desirable then use purpose=desktop
    variant('purpose', default='cluster', values=('cluster', 'desktop'),
            description="build relion for use in cluster or desktop")
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'Profiling', 'Benchmarking'))

    depends_on('mpi')
    # relion will not build with newer versions of cmake
    # per https://github.com/3dem/relion/issues/380
    depends_on('cmake@3:3.9.4', type='build')
    depends_on('fftw+float+double')
    depends_on('fltk', when='+gui')
    depends_on('libtiff')

    # relion 3 supports cuda 9
    # relion < 3 does not
    depends_on('cuda', when='+cuda')
    depends_on('cuda@9:', when='@3: +cuda')
    depends_on('cuda@8.0:8.99', when='@:2 +cuda')

    def cmake_args(self):

        carch = self.spec.variants['cuda_arch'].value[0]

        args = [
            '-DCMAKE_C_FLAGS=-g',
            '-DCMAKE_CXX_FLAGS=-g',
            '-DGUI=%s' % ('+gui' in self.spec),
            '-DDoublePrec_CPU=%s' % ('+double' in self.spec),
            '-DDoublePrec_GPU=%s' % ('+double-gpu' in self.spec),
        ]

        if '+cuda' in self.spec:
            # relion+cuda requires selecting cuda_arch
            if not carch:
                raise ValueError("select cuda_arch when building with +cuda")
            else:
                args += ['-DCUDA=ON', '-DCudaTexture=ON',
                         '-DCUDA_ARCH=%s' % (carch)]

        # these new values were added in relion 3
        # do not seem to cause problems with < 3
        else:
            args += ['-DMKLFFT=ON', '-DFORCE_OWN_TBB=ON', '-DALTCPU=ON']

        return args
