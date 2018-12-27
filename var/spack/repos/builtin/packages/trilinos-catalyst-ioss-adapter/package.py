# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TrilinosCatalystIossAdapter(CMakePackage):
    """Adapter for Trilinos Seacas Ioss and Paraview Catalyst"""

    homepage = "https://trilinos.org/"
    url      = "https://github.com/trilinos/Trilinos/archive/trilinos-release-12-12-1.tar.gz"
    git      = "https://github.com/trilinos/Trilinos.git"

    version('develop', branch='develop')
    version('master', branch='master')

    depends_on('bison')
    depends_on('flex')
    depends_on('paraview+mpi+python+osmesa')
    depends_on('py-numpy')
    # Here we avoid paraview trying to use netcdf~parallel-netcdf
    # which is netcdf's default, even though paraview depends on 'netcdf'
    # without any variants. Concretizer bug?
    depends_on('netcdf+parallel-netcdf')

    root_cmakelists_dir = 'packages/seacas/libraries/ioss/src/visualization/ParaViewCatalystIossAdapter'

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PYTHONPATH', join_path(self.prefix, 'python'))

    def cmake_args(self):
        spec = self.spec
        options = []

        paraview_version = 'paraview-%s' % spec['paraview'].version.up_to(2)

        options.extend([
            '-DParaView_DIR:PATH=%s' %
            spec['paraview'].prefix + '/lib/cmake/' + paraview_version
        ])

        return options
