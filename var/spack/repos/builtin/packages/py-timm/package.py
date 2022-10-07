# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTimm(PythonPackage):
    """(Unofficial) PyTorch Image Models."""

    homepage = "https://github.com/rwightman/pytorch-image-models"
    pypi = "timm/timm-0.4.12.tar.gz"

    version("0.5.4", sha256="5d7b92e66a76c432009aba90d515ea7a882aae573415a7c5269e3617df901c1f")
    version("0.4.12", sha256="b14be70dbd4528b5ca8657cf5bc2672c7918c3d9ebfbffe80f4785b54e884b1e")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.4:", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
    # https://github.com/rwightman/pytorch-image-models/pull/1256
    depends_on("pil@:9", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
