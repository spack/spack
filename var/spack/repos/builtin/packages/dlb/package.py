# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dlb(AutotoolsPackage):
    """DLB is a dynamic library designed to speed up HPC hybrid applications
    (i.e., two levels of parallelism) by improving the load balance of the
    outer level of parallelism (e.g., MPI) by dynamically redistributing the
    computational resources at the inner level of parallelism (e.g., OpenMP).
    at run time."""

    homepage = "https://pm.bsc.es/dlb"
    url = "https://pm.bsc.es/ftp/dlb/releases/dlb-3.2.tar.gz"
    git = "https://github.com/bsc-pm/dlb.git"

    maintainers("vlopezh")

    version("main", branch="main")
    version("3.2", sha256="b1c65ce3179b5275cfdf0bf921c0565a4a3ebcfdab72d7cef014957c17136c7e")
    version("3.1", sha256="d63ee89429fdb54af5510ed956f86d11561911a7860b46324f25200d32d0d333")
    version("3.0.2", sha256="75b6cf83ea24bb0862db4ed86d073f335200a0b54e8af8fee6dcf32da443b6b8")
    version("3.0.1", sha256="04f8a7aa269d02fc8561d0a61d64786aa18850367ce4f95d086ca12ab3eb7d24")
    version("3.0", sha256="e3fc1d51e9ded6d4d40d37f8568da4c4d72d1a8996bdeff2dfbbd86c9b96e36a")

    variant("debug", default=False, description="Builds additional debug libraries")
    variant("mpi", default=False, description="Builds MPI libraries")

    depends_on("mpi", when="+mpi")
    depends_on("python", type="build")
    depends_on("autoconf", type="build", when="@main")
    depends_on("automake", type="build", when="@main")
    depends_on("libtool", type="build", when="@main")

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("debug"))
        args.extend(self.enable_or_disable("instrumentation-debug", variant="debug"))
        args.extend(self.with_or_without("mpi"))

        return args
