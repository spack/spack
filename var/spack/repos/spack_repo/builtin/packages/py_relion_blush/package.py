# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyRelionBlush(PythonPackage):
    """Blush Refinement for Relion."""

    homepage = "https://github.com/3dem/relion-blush"

    url = "https://github.com/3dem/relion-blush"
    git = "https://github.com/3dem/relion-blush.git"

    license("MIT", checked_by="github_user1")

    version("20240529", commit="7889199242ab8227c628df72ea396826ed50185e")

    depends_on("py-setuptools", type="build")

    depends_on("py-torch@2.0.1:", type=("build", "run"))
    depends_on("py-torchvision@0.15.2:", type=("build", "run"))
    depends_on("py-numpy@1.24.4:", type=("build", "run"))
