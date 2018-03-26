##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Serban Maerean, serban@us.ibm.com, All rights reserved.
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


class Occa(Package):
    """OCCA is an open-source library that facilitates programming
    in an environment containing different types of devices.
    We abstract devices and let the user pick at run-time.
    For example: CPUs, GPUs, Intel's Xeon Phi, FPGAs.
    """

    homepage = "http://www.example.com"
    url      = "https://github.com/libocca/occa/archive/v1.0.0-alpha.4.tar.gz"

    version('1.0.0-alpha.4', '74e5adeba977e850802855c5be34e41d')

    variant('openmp', default=False,
            description='Enable OpenMP backend')
    variant('opencl', default=False,
            description='Enable OpenCL backend')
    variant('cuda', default=False,
            description='Enable CUDA backend')

    depends_on('cuda', when='+cuda')
    depends_on('opencl', when='+opencl')

    def install(self, spec, prefix):
        include_path = []
        library_path = []
        if '+opencl' in spec:
            include_path.append(spec['opencl'].prefix.include)
            library_path.append(spec['opencl'].prefix.lib)
        if '+cuda' in spec:
            include_path.append(spec['cuda'].prefix.include)
            library_path.append(spec['cuda'].prefix.lib)

        import sys
        sys.stderr.write('OCCA_INCLUDE_PATH=' + ':'.join(include_path))
        sys.stderr.write('OCCA_LIBRARY_PATH=' + ':'.join(library_path))

        make('all',
             'OCCA_INCLUDE_PATH=' + ':'.join(include_path),
             'OCCA_LIBRARY_PATH=' + ':'.join(library_path))
        for path in ['bin', 'include', 'lib', 'scripts']:
            install_tree(path, join_path(prefix, path))
