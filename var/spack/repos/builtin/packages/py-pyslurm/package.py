# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyPyslurm(PythonPackage):
    """PySlurm is the Python client library for the Slurm HPC Scheduler."""

    homepage = "https://pyslurm.github.io/"

    url = "https://github.com/PySlurm/pyslurm/archive/refs/tags/v23.2.0.tar.gz"

    version("23.2.2", sha256="f6db911515027ce5bfda7d3bc8e58935f48b20e4b6a0f98604e1de6043fa8a62")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-wheel@0.37.0", type="build")
    depends_on("py-cython@0.29.30:2", type="build")
    depends_on("py-setuptools@59.2.0", type="build")

    depends_on("slurm@23.02.0:23.02", type=("build", "run"))

    # fix from https://github.com/PySlurm/pyslurm/pull/325
    patch("kill-job-array-v23.2.2.patch", when="@23.2.2")

    def setup_build_environment(self, env):
        prefix = self.spec["slurm"].prefix
        # spack installed -> lib
        # rpm installed -> probably lib64
        for lib in "lib", "lib64":
            lib_dir = join_path(prefix, lib)
            lib_slurm = join_path(lib_dir, "slurm")
            if os.path.isdir(lib_slurm):
                env.set("SLURM_LIB_DIR", lib_dir)
                break
        env.set("SLURM_INCLUDE_DIR", prefix.include)
