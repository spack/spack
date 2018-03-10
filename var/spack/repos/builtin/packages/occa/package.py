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
import shutil


class Occa(Package):
    """OCCA is an open-source (MIT license) library used to program current
       multi-core/many-core architectures. Devices (such as CPUs, GPUs,
       Intel's Xeon Phi, FPGAs, etc) are abstracted using an offload-model
       for application development and programming for the devices is done
       through a C-based (OKL) or Fortran-based kernel language (OFL).
       OCCA gives developers the ability to target devices at run-time by
       using run-time compilation for device kernels.
    """

    homepage = "http://libocca.org"

    version('develop', git='https://github.com/libocca/occa.git')
    version('0.2', git='https://github.com/libocca/occa.git', tag='0.2')
    version('0.1', git='https://github.com/libocca/occa.git', tag='0.1')
    version('0.0.0', git='https://github.com/libocca/occa.git',
            commmit='381e886886dc87823769c5f20d0ecb29dd117afa')

    variant('cuda',   default=True,
            description='Activates support for CUDA')
    variant('openmp',   default=False,
            description='Activates support for OpenMP')
    variant('opencl',   default=False,
            description='Activates support for OpenCL')
    variant('coi',   default=False,
            description='Activates support for COI')
    depends_on('cuda', when='+cuda')

    def install(self, spec, prefix):
        os.environ['OCCA_CXX'] = self.compiler.cxx
        # TODO: How can I get all the Cxx flags that Spack is using?
        # os.environ['OCCA_CXXFLAGS'] =
        os.environ['OCCA_CUDA_COMPILER'] = os.path.join(spec['cuda'].prefix, 'bin', 'nvcc')
        # TODO: Set variables for the other variants
        make()
        shutil.copytree('lib', os.path.join(prefix, 'lib'))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Set up OCCA_DIR for everyone using the OCCA library
        spack_env.set('OCCA_DIR', os.path.join(self.prefix, 'lib'))
