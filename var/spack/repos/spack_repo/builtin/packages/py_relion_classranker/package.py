# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyRelionClassranker(PythonPackage):
    """The class ranker is part of the cryogenic electron microscopy (cryo-EM)
    dataset processing pipeline in RELION. It is used to automatically
    select suitable particles (EM images) assigned to 2D class averages
    for further downstream processing."""

    homepage = "https://github.com/3dem/relion-classranker"

    url = "https://github.com/3dem/relion-classranker"
    git = "https://github.com/3dem/relion-classranker.git"

    license("GPL-3.0-only", checked_by="snehring")

    version("20250108", commit="8727e78cf00ffcbb0cb3dd5918db987a13cf4f3a")

    depends_on("py-setuptools", type="build")

    depends_on("py-torch@2.0.1:", type=("build", "run"))
    depends_on("py-torchvision@0.15.2:", type=("build", "run"))
    depends_on("py-numpy@1.24.4", type=("build", "run"))
