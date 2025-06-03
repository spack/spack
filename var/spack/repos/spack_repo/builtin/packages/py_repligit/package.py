# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyRepligit(PythonPackage):
    """A Git client for mirroring multiple remotes without storing state."""

    homepage = "https://github.com/LLNL/repligit"
    pypi = "repligit/repligit-0.1.0.tar.gz"
    git = "https://github.com/LLNL/repligit.git"

    maintainers("alecbcs", "cmelone")

    license("Apache-2.0 WITH LLVM-exception")

    version("main", branch="main")
    version("0.1.1", sha256="e1fec2b080dd657502b967148fbb7dd5d33eb02fc47a2e91ed7bbfebf082410e")
    version("0.1.0", sha256="9beac1a14542704f2e5af6a2f3d391d8adf2112ae3c70e98339db251a9e1079e")

    variant("aiohttp", default="False", description="Enable aiohttp support")

    conflicts("python@:3.12", when="@0.1.0")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-hatchling", type="build")

    depends_on("py-aiohttp", type=("build", "run"), when="+aiohttp")
