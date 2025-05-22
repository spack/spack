# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Melissa(CMakePackage):
    """Melissa is a file-avoiding, adaptive, fault-tolerant and elastic
    framework, to run large-scale sensitivity analysis on supercomputers.
    """

    homepage = "https://gitlab.inria.fr/melissa/melissa"
    git = "https://gitlab.inria.fr/melissa/melissa.git"

    # FIXME: Replace with an official link
    url = "https://gitlab.inria.fr/melissa/melissa/-/archive/ac-develop-stable/melissa-ac-develop-stable.tar.gz"
    # attention: Git**Hub**.com accounts
    maintainers("abhishekp1297", "viperML", "raffino")

    version("develop", branch="develop", preferred=True)
    version(
        "0.7.1",
        sha256="c30584f15fecf6297712a88e4d28851bfd992f31209fd7bb8af2feebe73d539d",
        deprecated=True,
    )
    version(
        "0.7.0",
        sha256="a801d0b512e31a0750f98cfca80f8338985e06abf9b26e96f7645a022864e41c",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.15:", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libzmq@4.2:4", type=("build", "run"))
    depends_on("python@3.9:3.12", type=("build", "run"))
    depends_on("mpi", type=("build", "run"))

    def setup_run_environment(self, env):
        python = self.spec["python"]
        python_version = python.version.up_to(2)
        # This path points to the python client API scripts installed in $CMAKE_INSTALL_PREFIX/lib
        melissa_api_site_packages = f"{self.prefix.lib}/python{python_version}/site-packages"
        env.prepend_path("PYTHONPATH", melissa_api_site_packages)
