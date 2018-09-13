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


class Moab(AutotoolsPackage):
    """MOAB is a component for representing and evaluating mesh
    data. MOAB can store structured and unstructured mesh, consisting
    of elements in the finite element 'zoo.' The functional interface
    to MOAB is simple yet powerful, allowing the representation of
    many types of metadata commonly found on the mesh. MOAB is
    optimized for efficiency in space and time, based on access to
    mesh in chunks rather than through individual entities, while also
    versatile enough to support individual entity access."""

    homepage = "https://bitbucket.org/fathomteam/moab"
    url = "http://ftp.mcs.anl.gov/pub/fathom/moab-5.0.0.tar.gz"

    version('5.0.0', '1840ca02366f4d3237d44af63e239e3b')
    version('4.9.2', '540931a604c180bbd3c1bb3ee8c51dd0')
    version('4.9.1', '19cc2189fa266181ad9109b18d0b2ab8')
    version('4.9.0', '40695d0a159040683cfa05586ad4a7c2')
    version('4.8.2', '1dddd10f162fce3cfffaedc48f6f467d')

    variant('mpi', default=True, description='enable mpi support')
    variant('hdf5', default=True,
            description='Required to enable the hdf5 (default I/O) format')
    variant('netcdf', default=False,
            description='Required to enable the ExodusII reader/writer.')
    variant('pnetcdf', default=False,
            description='Enable pnetcdf (AKA parallel-netcdf) support')
    variant('netcdf', default=False,
            description='Required to enable the ExodusII reader/writer.')
    variant('zoltan', default=False, description='Enable zoltan support')
    variant('cgm', default=False, description='Enable common geometric module')
    variant('metis', default=True, description='Enable metis link')
    variant('parmetis', default=True, description='Enable parmetis link')
    variant('irel', default=False, description='Enable irel interface')
    variant('fbigeom', default=False, description='Enable fbigeom interface')
    variant('coupler', default=True, description='Enable mbcoupler tool')

    variant("debug", default=False, description='enable debug symbols')
    variant('shared', default=False,
            description='Enables the build of shared libraries')
    variant('fortran', default=True, description='Enable Fortran support')

    conflicts('+irel', when='~cgm')
    conflicts('+pnetcdf', when='~mpi')
    conflicts('+parmetis', when='~mpi')
    conflicts('+coupler', when='~mpi')

    # There are many possible variants for MOAB. Here are examples for
    # two of them:
    #
    # variant('vtk', default=False, description='Enable VTK support')
    # variant('cgns', default=False, description='Enable CGNS support')
    # depends_on('cgns', when='+cgns')
    # depends_on('vtk', when='+vtk')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5', when='+hdf5')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('netcdf', when='+netcdf')
    depends_on('parallel-netcdf', when='+pnetcdf')
    depends_on('cgm', when='+cgm')
    depends_on('metis', when='+metis')
    depends_on('parmetis', when='+parmetis')
    # FIXME it seems that zoltan needs to be built without fortran
    depends_on('zoltan~fortran', when='+zoltan')

    def configure_args(self):
        spec = self.spec

        options = [
            '--enable-optimize',
            '--disable-vtkMOABReader',
            '--disable-mbtagprop',
            '--disable-mbmem',
            '--disable-spheredecomp',
            '--disable-mbsurfplot',
            '--disable-gsets',
            '--disable-mcnpmit',
            '--disable-refiner',
            '--disable-h5mtools',
            '--disable-mbcslam',
            '--with-pic',
            '--without-vtk'
        ]
        if '+mpi' in spec:
            options.extend([
                '--with-mpi=%s' % spec['mpi'].prefix,
                'CXX=%s' % spec['mpi'].mpicxx,
                'CC=%s' % spec['mpi'].mpicc,
                'FC=%s' % spec['mpi'].mpifc
            ])
            if '+parmetis' in spec:
                options.append('--with-parmetis=%s' % spec['parmetis'].prefix)
            else:
                options.append('--without-parmetis')
#          FIXME: --without-mpi does not configure right
#       else:
#           options.append('--without-mpi')

        options.append('--with-blas=%s' % spec['blas'].libs.ld_flags)
        options.append('--with-lapack=%s' % spec['lapack'].libs.ld_flags)

        if '+hdf5' in spec:
            options.append('--with-hdf5=%s' % spec['hdf5'].prefix)
        else:
            options.append('--without-hdf5')

        if '+netcdf' in spec:
            options.append('--with-netcdf=%s' % spec['netcdf'].prefix)
        else:
            options.append('--without-netcdf')

        if '+pnetcdf' in spec:
            options.append('--with-pnetcdf=%s'
                           % spec['parallel-netcdf'].prefix)
        else:
            options.append('--without-pnetcdf')

        if '+cgm' in spec:
            options.append('--with-cgm=%s' % spec['cgm'].prefix)
            if '+irel' in spec:
                options.append('--enable-irel')
            else:
                options.append('--disable-irel')
        else:
            options.append('--without-cgm')
        if '+fbigeom' in spec:
            options.append('--enable-fbigeom')
        else:
            options.append('--disable-fbigeom')

        if '+coupler' in spec:
            options.append('--enable-mbcoupler')
        else:
            options.append('--disable-mbcoupler')

        if '+metis' in spec:
            options.append('--with-metis=%s' % spec['metis'].prefix)
        else:
            options.append('--without-metis')

        if '+parmetis' in spec:
            options.append('--with-parmetis=%s' % spec['parmetis'].prefix)
        else:
            options.append('--without-parmetis')

        if '+zoltan' in spec:
            options.append('--with-zoltan=%s' % spec['zoltan'].prefix)
        else:
            options.append('--without-zoltan')

        if '+debug' in spec:
            options.append('--enable-debug')
        else:
            options.append('--disable-debug')

        # FIXME it seems that with cgm and shared, we have a link
        #   issue  in tools/geometry
        if '+shared' in spec:
            options.append('--enable-shared')
        else:
            options.append('--disable-shared')

        if '~fortran' in spec:
            options.append('--disable-fortran')
        else:
            options.append('--enable-fortran')

        return options

    # FIXME Run the install phase with -j 1.  There seems to be a problem with
    # parallel installations of examples
    def install(self, spec, prefix):
        make('install', parallel=False)
