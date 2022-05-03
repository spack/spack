# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Boxmg4wrf(MakefilePackage):
    """This is a version of the Dendy-Moulton "Black Box Multigrid" elliptic
    equation solver (until a more permanent archive is established). It has
    been updated to allow single-precision solutions and is posted here for
    use with an upcoming release of WRF (Weather Research and Forecasting)
    model including storm electrification. Only runs under MPI at this time
    (i.e., no SMP/OpenMP support)."""

    homepage = "https://sourceforge.net/projects/boxmg4wrf/"
    git      = "https://git.code.sf.net/p/boxmg4wrf/git"

    parallel = False

    # maintainers = ['github_user1', 'github_user2']

    version('master', branch='master')

    # Always allow argument mismatch. Yes, this is done because
    # this package overrides host FFLAGS/F90FLAGS
    patch('fallow_argument_mismatch.patch', when='%gcc@10:')
    patch('fallow_argument_mismatch.patch', when='%clang@11:')
    patch('fallow_argument_mismatch.patch', when='apple-clang@11:')

    depends_on('mpi')

    def install(self, spec, prefix):
        make()

        mkdirp(prefix.include)
        install_tree('include', prefix.include)

        mkdirp(prefix.lib)
        install_tree('lib', prefix.lib)

        mkdirp(prefix.extras)
        install_tree('extras', prefix.extras)

    def setup_run_environment(self, env):
        env.set('BOXMGLIBDIR', self.prefix)
