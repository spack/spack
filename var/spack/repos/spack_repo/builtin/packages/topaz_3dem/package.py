# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class Topaz3dem(PythonPackage):
    """topaz: Pipeline for particle picking in cryo-electron microscopy images using
    convolutional neural networks trained from positive and unlabeled examples. Also
    featuring micrograph and tomogram denoising with DNNs."""

    homepage = "https://github.com/3dem/topaz"
    git = "https://github.com/3dem/topaz.git"

    license("GPL-3.0-or-later")

    version("20220325", commit="14b2bc331768b67b3267397523de57c707fa1253")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1:2.3", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    depends_on("py-numpy@1.11:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scikit-learn@0.19.0:", type=("build", "run"))
    depends_on("py-scipy@0.17.0:", type=("build", "run"))
    depends_on("py-pillow@6.2.0:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
