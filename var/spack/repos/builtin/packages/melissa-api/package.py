# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MelissaApi(CMakePackage):
    """Melissa is a file-avoiding, adaptive, fault-tolerant and elastic
    framework, to run large-scale sensitivity analysis or deep-surrogate
    training on supercomputers.
    This package builds the API used when instrumenting the clients.
    """

    homepage = "https://gitlab.inria.fr/melissa/melissa"
    git = "https://gitlab.inria.fr/melissa/melissa.git"
    maintainers("robcaulk", "mschouler", "raffino")

    version("develop", branch="develop")

    depends_on("cmake@3.7.2:", type="build")
    depends_on("libzmq@4.1.5:")
    depends_on("mpi")

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.lib)
