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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install raja
#
# You can edit this file again by typing:
#
#     spack edit raja
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Raja(CMakePackage):
    """A performance portable parallel programming framework with focus on ease of development"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://github.com/LLNL/RAJA"
    url      = "https://github.com/LLNL/RAJA/archive/v0.2.5.zip"

    version('0.2.5', 'ec326e2938d1505078aa60cdfeaf48d0')
    version('0.2.4', '9facff6cb5bc163fda147f9718fc34f6')
    version('0.2.3', 'dabfcf6c95867dc0c01bae0d7ba3b964')
    version('0.2.2', '60835e76094751d8719311bc4236ce4d')
    version('0.2.1', '35741363f8b912c7f11685602a568d0f')
    version('0.2.0', 'ed076fafc8cfa03f4badec10dee729fb')
    version('0.1.0', 'a05098246c9dea465bcfd46b1268e517')

    variant('RAJA_ENABLE_EXAMPLES', default ="ON")
    variant('RAJA_REPORT_FT', default ="OFF")
    variant('RAJA_CUDA_ARCH', default ="sm_35")
    variant('RAJA_USE_GETTIME', default ="OFF")
    variant('RAJA_COHERENCE_BLOCK_SIZE', default ="64")
    variant('RAJA_DATA_ALIGN', default ="64")
    variant('RAJA_RANGE_ALIGN', default ="4")
    variant('RAJA_ENABLE_CLANG_CUDA', default ="OFF")
    variant('RAJA_ENABLE_OPENMP', default ="ON")
    variant('RAJA_ENABLE_CILK', default ="OFF")
    variant('RAJA_USE_COMPLEX', default ="OFF")
    variant('RAJA_ENABLE_DOCUMENTATION', default ="OFF")
    variant('RAJA_ENABLE_NESTED', default ="OFF")
    variant('RAJA_USE_CLOCK', default ="OFF")
    variant('RAJA_RANGE_MIN_LENGTH', default ="32")
    variant('RAJA_USE_DOUBLE', default ="OFF")
    variant('RAJA_ENABLE_TESTS', default ="ON")
    variant('RAJA_ENABLE_WARNINGS', default ="OFF")
    variant('RAJA_USE_CHRONO', default ="ON")
    variant('RAJA_TIMER', default ="chrono")
    variant('RAJA_ENABLE_FT', default ="OFF")
    variant('RAJA_ENABLE_CUDA', default ="OFF")
    variant('RAJA_USE_FLOAT', default ="OFF")
    variant('TEST_DRIVER', default ="")
    def cmake_args(self):
        args = [ '-DRAJA_ENABLE_EXAMPLES:BOOL=%s' % self.spec.variants['RAJA_ENABLE_EXAMPLES'].value,
                 '-DRAJA_REPORT_FT:BOOL=%s' % self.spec.variants['RAJA_REPORT_FT'].value,
                 '-DRAJA_CUDA_ARCH:STRING=%s' % self.spec.variants['RAJA_CUDA_ARCH'].value,
                 '-DRAJA_USE_GETTIME:BOOL=%s' % self.spec.variants['RAJA_USE_GETTIME'].value,
                 '-DRAJA_COHERENCE_BLOCK_SIZE:STRING=%s' % self.spec.variants['RAJA_COHERENCE_BLOCK_SIZE'].value,
                 '-DRAJA_DATA_ALIGN:STRING=%s' % self.spec.variants['RAJA_DATA_ALIGN'].value,
                 '-DRAJA_RANGE_ALIGN:STRING=%s' % self.spec.variants['RAJA_RANGE_ALIGN'].value,
                 '-DRAJA_ENABLE_CLANG_CUDA:BOOL=%s' % self.spec.variants['RAJA_ENABLE_CLANG_CUDA'].value,
                 '-DRAJA_ENABLE_OPENMP:BOOL=%s' % self.spec.variants['RAJA_ENABLE_OPENMP'].value,
                 '-DRAJA_ENABLE_CILK:BOOL=%s' % self.spec.variants['RAJA_ENABLE_CILK'].value,
                 '-DRAJA_USE_COMPLEX:BOOL=%s' % self.spec.variants['RAJA_USE_COMPLEX'].value,
                 '-DRAJA_ENABLE_DOCUMENTATION:BOOL=%s' % self.spec.variants['RAJA_ENABLE_DOCUMENTATION'].value,
                 '-DRAJA_ENABLE_NESTED:BOOL=%s' % self.spec.variants['RAJA_ENABLE_NESTED'].value,
                 '-DRAJA_USE_CLOCK:BOOL=%s' % self.spec.variants['RAJA_USE_CLOCK'].value,
                 '-DRAJA_RANGE_MIN_LENGTH:STRING=%s' % self.spec.variants['RAJA_RANGE_MIN_LENGTH'].value,
                 '-DRAJA_USE_DOUBLE:BOOL=%s' % self.spec.variants['RAJA_USE_DOUBLE'].value,
                 '-DRAJA_ENABLE_TESTS:BOOL=%s' % self.spec.variants['RAJA_ENABLE_TESTS'].value,
                 '-DRAJA_ENABLE_WARNINGS:BOOL=%s' % self.spec.variants['RAJA_ENABLE_WARNINGS'].value,
                 '-DRAJA_USE_CHRONO:BOOL=%s' % self.spec.variants['RAJA_USE_CHRONO'].value,
                 '-DRAJA_TIMER:STRING=%s' % self.spec.variants['RAJA_TIMER'].value,
                 '-DRAJA_ENABLE_FT:BOOL=%s' % self.spec.variants['RAJA_ENABLE_FT'].value,
                 '-DRAJA_ENABLE_CUDA:BOOL=%s' % self.spec.variants['RAJA_ENABLE_CUDA'].value,
                 '-DRAJA_USE_FLOAT:BOOL=%s' % self.spec.variants['RAJA_USE_FLOAT'].value,
                 '-DTEST_DRIVER:STRING=%s' % self.spec.variants['TEST_DRIVER'].value,
               ]
        return args
