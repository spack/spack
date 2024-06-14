# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    git = "https://git.code.sf.net/p/boxmg4wrf/git"

    parallel = False

    version("master", branch="master")

    depends_on("mpi")

    def flag_handler(self, name, flags):
        if name in ["fcflags", "fflags"] and self.spec.satisfies("%gcc@10:"):
            flags.append("-fallow-argument-mismatch -fallow-invalid-boz")
        return (flags, None, None)

    def install(self, spec, prefix):
        make()

        mkdirp(prefix.include)
        install_tree("include", prefix.include)

        mkdirp(prefix.lib)
        install_tree("lib", prefix.lib)

        mkdirp(prefix.extras)
        install_tree("extras", prefix.extras)

    def setup_run_environment(self, env):
        env.set("BOXMGLIBDIR", self.prefix)
