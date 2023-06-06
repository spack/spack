# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PySmartsim(PythonPackage):
    """A workflow library to easily integrate machine learning libraries with
    high performance computing simulations and applications
    """

    homepage = "https://www.craylabs.org/docs/overview.html"
    git = "https://github.com/CrayLabs/SmartSim"
    pypi = "smartsim/smartsim-0.4.2.tar.gz"

    maintainers("MattToast")

    version("0.5.0", sha256="35b36243dc84af62261a7f772bae92f0b3502faf01401423899cb2a48339858c")
    version("0.4.2", sha256="ab632ff7d036e73822ddc5081fe85ea69c48d8be53ad0e6e487e9193eb3410f6")

    variant("torch", default=True, description="Build with the pytorch backend")
    variant("cuda", default=False, description="Use CUDA")
    variant("rocm", default=False, description="Use ROCm")

    depends_on("python@3.8:3.10", type=("build", "run"))
    depends_on("py-wheel", type=("build",))
    depends_on("py-setuptools", type=("build",))

    depends_on("py-psutil@5.7.2:", type=("build", "run"))
    depends_on("py-coloredlogs@10:", type=("build", "run"))
    depends_on("py-tabulate@0.8.9:", type=("build", "run"))
    depends_on("py-redis@4.5:", type=("build", "run"))
    depends_on("py-tqdm@4.56:", type=("build", "run"))
    depends_on("py-filelock@3.4:", type=("build", "run"))
    depends_on("py-protobuf@3.20:3", type=("build", "run"))

    # Companion libs
    depends_on("py-smartredis@0.4.1", type=("build", "run"), when="@0.5.0")
    depends_on("py-smartredis@0.4.0", type=("build", "run"), when="@0.4.2")

    # Backends
    depends_on("redis@7.0.5:", type=("build", "run"))

    depends_on("redis-ai@1.2.7:", type=("build", "run"))
    depends_on("redis-ai+cuda", type=("build", "run"), when="+cuda")
    depends_on("redis-ai+rocm", type=("build", "run"), when="+rocm")

    # ML Deps
    with when("+torch"):
        depends_on("redis-ai+torch", type=("build", "run"))
        depends_on("py-torch@1.11:", type=("build", "run"))
        depends_on("py-torch+cuda+cudnn", type=("build", "run"), when="+cuda")
        depends_on("py-torch+rocm", type=("build", "run"), when="+rocm")

    # By default, the SmartSim `setup.py` will attempt to fetch and build
    # its own copy of Redis. This should be patched out and the version of
    # Redis retrieved through spack should be used instead.
    patch("ss-dont-build-db.patch")

    # SmartSim provides its own CLI to fetch and build its own
    # copy of Redis, RedisAI, and ML deps. This functionality should be
    # patched out so that users do not accidentally overwrite/break
    # dependencies fetched though Spack
    patch("ss-0-5-0-remove-typed-cli-build-fns.patch", when="@0.5.0")
    patch("ss-0-4-2-remove-cli-build-fns.patch", when="@0.4.2")

    # SmartSim v0.4.2 uses a now deprecated package `redis-py-cluster` that is
    # not currently offered through Spack. This functionality was since migrated
    # to the `redis` package in v3.0 which is already a dependency for SS v0.4.2.
    # This patch will simply make the needed namespace changes to remove this dep.
    patch("ss-0-4-2-remove-redis-py-cluster.patch", when="@0.4.2")

    @run_after("install")
    def symlink_bin_deps(self):
        ss_core_path = join_path(
            self.prefix, self.spec["python"].package.purelib, "smartsim", "_core"
        )
        os.symlink(
            self.spec["redis"].prefix.bin.join("redis-server"),
            join_path(ss_core_path, "bin", "redis-server"),
        )
        os.symlink(
            self.spec["redis"].prefix.bin.join("redis-cli"),
            join_path(ss_core_path, "bin", "redis-cli"),
        )
        os.symlink(self.spec["redis-ai"].prefix, join_path(ss_core_path, "lib"))
