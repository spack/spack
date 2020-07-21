# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Elmerfem(CMakePackage):
    """Elmer is an open source multiphysical simulation software. It
    includes physical models of fluid dynamics, structural mechanics,
    electromagnetics, heat transfer and acoustics."""

    homepage = "https://www.csc.fi/web/elmer"
    url      = "https://github.com/ElmerCSC/elmerfem/archive/release-8.4.tar.gz"

    version('8.4', sha256='cc3ce807d76798361592cc14952cdc3db1ad8f9bac038017514033ce9badc5b3')
    version('devel', git='https://github.com/ElmerCSC/elmerfem.git', branch='devel')

    variant('openmp', default=True, description='Enable OpenMP support.')
    variant('mumps', default=False, description='Enable MUMPS support.')
    variant('hypre', default=False, description='Enable Hypre support.')
    variant('trilinos', default=False, description='Enable Trilinos support.')
    variant('zoltan', default=False, description='Enable Zoltan support.')
    variant('lua', default=False, description='Enable Lua support.')

    depends_on('mpi')
    depends_on('netcdf-fortran')
    depends_on('blas')
    depends_on('lapack')
    depends_on('mumps', when='+mumps')
    depends_on('hypre', when='+hypre')
    depends_on('trilinos~hypre~zoltan~zoltan2', when='+trilinos')
    depends_on('zoltan+fortran', when='+zoltan')
    depends_on('lua@5.1.5', when='+lua')

    def cmake_args(self):

        spec = self.spec

        args = ['-DWITH_ElmerIce=ON', '-DWITH_CONTRIB=ON', '-DWITH_MPI=ON']

        if '+openmp' in spec:
            args.append('-DWITH_OpenMP=ON')
        else:
            args.append('-DWITH_OpenMP=OFF')

        if '+mumps' in spec:
            args.append('-DWITH_Mumps=ON')
        else:
            args.append('-DWITH_Mumps=OFF')

        if '+hypre' in spec:
            args.append('-DWITH_Hypre=ON')
        else:
            args.append('-DWITH_Hypre=OFF')

        if '+trilinos' in spec:
            args.extend([
                '-DWITH_Trilinos=ON',
                '-DCMAKE_CXX_STANDARD=11',
            ])
        else:
            args.append('-DWITH_Trilinos=OFF')

        if '+lua' in spec:
            args.extend([
                '-DWITH_LUA=ON',
                '-DUSE_SYSTEM_LUA=ON'
            ])
            if '%gcc' in spec:
                args.append('-DCMAKE_Fortran_FLAGS=-ffree-line-length-none')

        else:
            args.append('-DWITH_LUA=OFF')

        if '+zoltan' in spec:
            args.extend([
                '-DWITH_Zoltan=ON',
                '-DUSE_SYSTEM_ZOLTAN=ON'
            ])
        else:
            args.append('-DWITH_Zoltan=OFF')

        return args

    def setup_run_environment(self, env):
        env.set('ELMER_HOME', self.prefix)
