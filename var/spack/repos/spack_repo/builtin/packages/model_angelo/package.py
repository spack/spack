# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class ModelAngelo(PythonPackage):
    """ModelAngelo is an automatic atomic model building program for cryo-EM maps."""

    homepage = "https://github.com/3dem/model-angelo"

    url = "https://github.com/3dem/model-angelo"
    git = "https://github.com/3dem/model-angelo.git"

    license("MIT", checked_by="snehring")

    version("20250218", commit="ddd969038045c28c5f281353dd62e98afb57859c")

    depends_on("py-setuptools@:58", type="build")

    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-biopython@1.81:", type=("build", "run"))
    depends_on("py-einops", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-mrcfile", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-fair-esm@1.0.3", type=("build", "run"))
    depends_on("py-pyhmmer@0.7.1", type=("build", "run"))
    depends_on("py-loguru", type=("build", "run"))
    depends_on("py-numpy@1.24.4:", type=("build", "run"))
