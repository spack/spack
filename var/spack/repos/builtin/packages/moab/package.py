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


class Moab(Package):
    """MOAB is a component for representing and evaluating mesh
    data. MOAB can store structured and unstructured mesh, consisting
    of elements in the finite element 'zoo.' The functional interface
    to MOAB is simple yet powerful, allowing the representation of
    many types of metadata commonly found on the mesh. MOAB is
    optimized for efficiency in space and time, based on access to
    mesh in chunks rather than through individual entities, while also
    versatile enough to support individual entity access."""
    homepage = "https://bitbucket.org/fathomteam/moab"
    url      = "http://ftp.mcs.anl.gov/pub/fathom/moab-4.6.3.tar.gz"

    version('4.9.1', '19cc2189fa266181ad9109b18d0b2ab8')
    version('4.9.0', '40695d0a159040683cfa05586ad4a7c2')
    version('4.8.2', '1dddd10f162fce3cfffaedc48f6f467d')

    variant('netcdf', default=False,
            description='Required to enable the ExodusII reader/writer.')
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('fortran', default=True, description='Enable Fortran support')

    # There are many possible variants for MOAB. Here are examples for
    # two of them:
    #
    # variant('vtk', default=False, description='Enable VTK support')
    # variant('cgns', default=False, description='Enable CGNS support')
    # depends_on('cgns', when='+cgns')
    # depends_on('vtk', when='+vtk')

    depends_on('mpi')
    depends_on('hdf5+mpi')
    depends_on('netcdf+mpi', when='+netcdf')
    depends_on('parmetis')
    depends_on('zoltan')
    depends_on('zoltan~fortran', when='~fortran')

    def install(self, spec, prefix):

        options = [
            '--prefix=%s' % prefix,
            '--enable-optimize',
            '--enable-tools',
            '--with-pic',
            '--with-mpi=%s' % spec['mpi'].prefix,
            '--with-hdf5=%s' % spec['hdf5'].prefix,
            '--with-parmetis=%s' % spec['parmetis'].prefix,
            '--with-zoltan=%s' % spec['zoltan'].prefix,
            '--disable-vtkMOABReader',
            '--without-vtk',
            'CXX=%s' % spec['mpi'].mpicxx,
            'CC=%s' % spec['mpi'].mpicc,
            'FC=%s' % spec['mpi'].mpifc]

        if '~fortran' in spec:
            options.append('--disable-fortran')
        if '+shared' in spec:
            options.append('--enable-shared')
        if '+netcdf' in spec:
            options.append('--with-netcdf=%s' % spec['netcdf'].prefix)

        configure(*options)
        make()
        make('install')
