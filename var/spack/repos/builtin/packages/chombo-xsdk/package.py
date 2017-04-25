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
import glob
import os

class ChomboXsdk(Package):
    """Chombo is a ...
    """

    homepage = "http://chombo.lbl.gov/"
    url = "http://bitbucket.org/drhansj/chombo-xsdk/get/xsdk-0.2.0a.tar.bz2"

    version('xsdk-0.2.0', git='http://bitbucket.org/drhansj/chombo-xsdk.git', commit='8893c7')
    version('develop', git='http://bitbucket.org/drhansj/chombo-xsdk.git', tag='master')

    variant('dim'      , default=2    , description = 'Set the physical dimension')
    variant('debug'    , default=False, description = 'Build with debugging symbols')
    variant('opt'      , default=True , description = 'Build using compiler optimizations')
    variant('namespace', default=False, description = 'Put Chombo in a namespace')
    variant('mpi'      , default=True , description = 'Compile with MPI support')
    variant('use_eb'   , default=False, description = 'Compile with Embedded Boundary support')
    variant('use_hdf'  , default=True , description = 'Compile with HDF5 I/O support')
    variant('use_petsc', default=True , description = 'Compile with PETSc support')

    # Chombo dependencies for xSDK build
    depends_on('blas')
    depends_on('lapack')

    depends_on('mpi', when='+mpi')

    depends_on('hdf5~mpi', when='+use_hdf~mpi')
    depends_on('hdf5+mpi', when='+use_hdf+mpi')

    depends_on('petsc~mpi', when='+use_petsc~mpi')
    depends_on('petsc+mpi', when='+use_petsc+mpi')

    def install(self, spec, prefix):
        lapack_blas = spec['lapack'].libs + spec['blas'].libs

        options = []

        if 'dim' in spec:
          options.append('DIM=%d' % spec['dim'])

        if 'use_hdf' in spec:
          options.append('USE_HDF=TRUE')
          options.append('HDFINCFLAGS=-I%s/include' % spec['use_hdf',prefix])
          options.append('HDFLIBFLAGS=-L%s/lib -lhdf5 -lz' % spec['use_hdf',prefix])
          options.append('HDFMPIINCFLAGS=-I%s/include' % spec['use_hdf',prefix])
          options.append('HDFMPILIBFLAGS=-L%s/lib -lhdf5 -lz' % spec['use_hdf',prefix])
        else:
          options.append('USE_HDF=FALSE')

        if 'mpi' in spec:
          options.append('MPI=TRUE')
        else:
          options.append('MPI=FALSE')

        make('--directory=lib','lib',*options)

        # FIXME:
        # cd "EXAMPLE" do
        # system "make"

        # need to install by hand
        #headers_location = self.prefix.include
        #mkdirp(headers_location)
        #mkdirp(prefix.lib)

        #headers = glob.glob(join_path(self.stage.source_path, 'SRC', '*.h'))
        #for h in headers:
            #install(h, headers_location)

        #chomboxsdk_lib = join_path(self.stage.source_path,
                                    #'lib/libchombo_xsdk.a')
        #install(chomboxsdk_lib, self.prefix.lib)
