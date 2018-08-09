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


class Adios2(CMakePackage):
    """Next generation of ADIOS developed in the Exascale Computing Program"""

    homepage = "https://www.olcf.ornl.gov/center-projects/adios/"
    url      = "https://github.com/ornladios/ADIOS2/archive/v2.0.0.tar.gz"
    git      = "https://github.com/ornladios/ADIOS2.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('2.2.0', sha256='77058ea2ff7224dc02ea519733de42d89112cf21ffe7474fb2fa3c5696152948')
    version('2.1.0', '431fa5b015349f1838b96b8f5a1cc8f8')
    version('2.0.0', 'da39655b51745d2c5f3f1e46c5abc4d7')

    variant('shared', default=True,
            description='Also build shared libraries')
    variant('mpi', default=True,
            description='Enable MPI')
    # transforms
    variant('bzip2', default=True,
            description='Enable BZip2 compression')
    variant('zfp', default=True,
            description='Enable ZFP compression')
    # sz is broken in 2.2.0: https://github.com/ornladios/ADIOS2/issues/705
    # variant('sz', default=True,
    #         description='Enable SZ compression')
    # transport engines
    variant('dataman', default=True,
            description='Enable the DataMan engine for WAN transports')
    # currently required by DataMan, optional in the future
    # variant('zeromq', default=False,
    #         description='Enable ZeroMQ for the DataMan engine')
    variant('hdf5', default=False,
            description='Enable the HDF5 engine')
    variant('adios1', default=False,
            description='Enable the ADIOS 1.x engine')
    # language bindings
    variant('python', default=True,
            description='Enable the Python >= 2.7 bindings')
    variant('fortran', default=True,
            description='Enable the Fortran bindings')

    # requires mature C++11 implementations
    conflicts('%gcc@:4.7')
    conflicts('%intel@:15')
    conflicts('%pgi@:14')

    # DataMan needs dlopen
    conflicts('+dataman', when='~shared')

    depends_on('cmake@3.5.0:', type='build')
    depends_on('pkgconfig', type='build', when='@2.2.0:')
    # The included ffs requires bison and flex but using them makes
    # the build fail due to an undefined reference.
    # depends_on('bison', type='build', when='@2.2.0:')
    # depends_on('flex', when='@2.2.0:')

    # contained in thirdparty/
    # depends_on('googletest')
    # depends_on('pugixml')
    # depends_on('kwsys')
    # depends_on('nlohmann-json')
    # depends_on('pybind11@2.1.1:', when='+python')

    depends_on('mpi', when='+mpi')
    depends_on('zeromq', when='+dataman')

    depends_on('hdf5', when='+hdf5')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('adios', when='+adios1')
    depends_on('adios+mpi', when='+adios1+mpi')

    depends_on('bzip2', when='+bzip2')
    depends_on('zfp', when='+zfp')
    # depends_on('sz@:1.4.12', when='+sz')

    extends('python', when='+python')
    depends_on('python@2.7:', type=('build', 'run'), when='+python')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'), when='+python')
    depends_on('py-mpi4py@2.0.0:', type=('build', 'run'), when='+mpi +python')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DADIOS2_BUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DADIOS2_BUILD_TESTING=OFF',
            '-DADIOS2_USE_MPI={0}'.format(
                'ON' if '+mpi' in spec else 'OFF'),
            '-DADIOS2_USE_BZip2={0}'.format(
                'ON' if '+bzip2' in spec else 'OFF'),
            '-DADIOS2_USE_ZFP={0}'.format(
                'ON' if '+zfp' in spec else 'OFF'),
            '-DADIOS2_USE_SZ={0}'.format(
                'ON' if '+sz' in spec else 'OFF'),
            '-DADIOS2_USE_DataMan={0}'.format(
                'ON' if '+dataman' in spec else 'OFF'),
            '-DADIOS2_USE_ZeroMQ={0}'.format(
                'ON' if '+dataman' in spec else 'OFF'),
            '-DADIOS2_USE_HDF5={0}'.format(
                'ON' if '+hdf5' in spec else 'OFF'),
            '-DADIOS2_USE_ADIOS1={0}'.format(
                'ON' if '+adios1' in spec else 'OFF'),
            '-DADIOS2_USE_Python={0}'.format(
                'ON' if '+python' in spec else 'OFF'),
            '-DADIOS2_USE_Fortran={0}'.format(
                'ON' if '+fortran' in spec else 'OFF')
        ]
        if spec.satisfies('+python'):
            args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s'
                        % self.spec['python'].command.path)
        return args
