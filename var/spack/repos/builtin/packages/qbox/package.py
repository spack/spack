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


class Qbox(MakefilePackage):
    """Qbox is a C++/MPI scalable parallel implementation of first-principles
    molecular dynamics (FPMD) based on the plane-wave, pseudopotential
    formalism. Qbox is designed for operation on large parallel computers."""

    homepage = "http://qboxcode.org/"
    url      = "http://qboxcode.org/download/qbox-1.63.7.tgz"

    version('1.63.7', '6b0cf5656f816a1a59e22b268387af33')
    version('1.63.5', 'da3161ab6a455793f2133dd03c04077c')
    version('1.63.4', '8596f32c8fb7e7baa96571c655aaee07')
    version('1.63.2', '55e8f13f37c8e1f43ca831791e3af1da')
    version('1.63.0', '1436c884c553ab026b7f787307e5e6ed')
    version('1.62.3', 'f07e038ab92b85956794e91a40346dbf')
    version('1.60.9', '53b0df612e56bb65e8220d9d9dc8d395')
    version('1.60.4', '060846c9fa03b1f3d7d5ce24a9491de2')
    version('1.60.0', '3856cdc38a27dc17705844c4b9241a21')
    version('1.58.0', 'ec0e6b79fa0ed06742212b1142e36b6a')
    version('1.56.2', 'df7a4217d059a5d351d92e480ed14112')
    version('1.54.4', '8f1a23af7d871317de93810b664ad3aa')
    version('1.54.2', 'aeefee061255dbb36ca7e49378f63ad5')
    version('1.52.3', '1862f2b2056cdf49ec4f746d45a7f1a6')
    version('1.52.2', 'e406deb4c46176f1c15c226868bf61e2')
    version('1.50.4', 'b06ff877257884e4fac321fb5a486266')
    version('1.50.2', '171660b1bb5e57637f019fef055fb764')
    version('1.50.1', '1da528b39da134f86f134432e8fada79')
    version('1.47.0', '86f402651d440e05adc94168d6105da7')
    version('1.45.3', '73b99a73dcbb1b5be9f66f3284750205')
    version('1.45.1', '59e0c2583769b7586981c0d6ffa1b267')
    version('1.45.0', '2c5bfbadfffd330c8c2fe294a10a08e4')
    version('1.44.0', 'c46a2f0f68fe9229aa77779da188cea9')

    depends_on('mpi')
    depends_on('blas')
    depends_on('scalapack')
    depends_on('fftw')
    depends_on('xerces-c')

    build_directory = 'src'

    def edit(self, spec, prefix):
        with open('src/spack.mk', 'w') as mkfile:
            mkfile.write('CXX = {0}\n'.format(spec['mpi'].mpicxx))
            mkfile.write('LD = $(CXX)\n')
            qbox_libs = spec['fftw'].libs + spec['xerces-c'].libs + \
                spec['scalapack'].libs + spec['blas'].libs
            mkfile.write('LDFLAGS = {0}\n'.format(qbox_libs.ld_flags))
            mkfile.write('DFLAGS = {0}\n'.format(' -D'.join((
                '',
                '_LARGEFILE_SOURCE', 'USE_MPI', 'USE_XERCES',
                'XERCESC_3', 'MPICH_IGNORE_CXX_SEEK', 'SCALAPACK',
                'USE_FFTW3', 'FFTWMEASURE', 'FFTW3_2D', 'ADD_',
            ))))
            mkfile.write('CXXFLAGS = {0}\n'.format(' '.join((
                '-g', '-O3', '$(DFLAGS)',
            ))))
        filter_file('$(TARGET)', 'spack', 'src/Makefile', string=True)

    def install(self, spec, prefix):
        mkdir(prefix.src)
        install('src/qb', prefix.src)
        install_tree('test', prefix)
        install_tree('xml', prefix)
        install_tree('util', prefix)
