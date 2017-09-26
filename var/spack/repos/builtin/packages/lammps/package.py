##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
#
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import datetime as dt


class Lammps(CMakePackage):
    """LAMMPS stands for Large-scale Atomic/Molecular Massively
    Parallel Simulator. This package uses patch releases, not
    stable release.
    See https://github.com/LLNL/spack/pull/5342 for a detailed
    discussion.
    """
    homepage = "http://lammps.sandia.gov/"
    url      = "https://github.com/lammps/lammps/archive/patch_1Sep2017.tar.gz"

    version('20170922', '4306071f919ec7e759bda195c26cfd9a')
    version('20170901', '767e7f07289663f033474dfe974974e7')
    version('develop', git='https://github.com/lammps/lammps', branch='master')

    def url_for_version(self, version):
        vdate = dt.datetime.strptime(str(version), "%Y%m%d")
        return "https://github.com/lammps/lammps/archive/patch_{0}.tar.gz".format(
            vdate.strftime("%d%b%Y").lstrip('0'))

    supported_packages = ['voronoi', 'rigid', 'user-nc-dump', 'kspace',
                          'latte', 'user-atc', 'meam', 'manybody']

    for pkg in supported_packages:
        variant(pkg, default=False,
                description='Activate the {0} package'.format(pkg))
    variant('lib', default=True,
            description='Build the liblammps in addition to the executable')
    variant('mpi', default=True,
            description='Build with mpi')

    depends_on('mpi', when='+mpi')
    depends_on('fftw', when='+ksapce')
    depends_on('voropp', when='+voronoi')
    depends_on('netcdf+mpi', when='+user-nc-dump')
    depends_on('blas', when='+user-atc')
    depends_on('lapack', when='+user-atc')
    depends_on('latte', when='+latte')
    depends_on('blas', when='+latte')
    depends_on('lapack', when='+latte')

    conflicts('+latte', when='@:20170921')

    patch("lib.patch", when="@20170901")
    patch("660.patch", when="@20170922")

    root_cmakelists_dir = 'cmake'

    def cmake_args(self):
        spec = self.spec

        return [
            '-DBUILD_SHARED_LIBS={0}'.format(
                'ON' if '+lib' in spec else 'OFF'),
            '-DENABLE_MPI={0}'.format(
                'ON' if '+mpi' in spec else 'OFF'),
            '-DENABLE_RIGID={0}'.format(
                'ON' if '+rigid' in spec else 'OFF'),
            '-DENABLE_MEAM={0}'.format(
                'ON' if '+meam' in spec else 'OFF'),
            '-DENABLE_KSAPCE={0}'.format(
                'ON' if '+kspace' in spec else 'OFF'),
            '-DFFT=FFTW3',  # doesn't do harm withiout KSPACE
            '-DENABLE_LATTE={0}'.format(
                'ON' if '+latte' in spec else 'OFF'),
            '-DENABLE_MANYBODY={0}'.format(
                'ON' if '+manybody' in spec else 'OFF'),
            '-DENABLE_USER-NETCDF={0}'.format(
                'ON' if '+user-nc-dump' in spec else 'OFF'),
            '-DENABLE_VORONOI={0}'.format(
                'ON' if '+voronoi' in spec else 'OFF'),
            '-DENABLE_USER-ATC={0}'.format(
                'ON' if '+user-atc' in spec else 'OFF'),
        ]
