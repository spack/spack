# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorflowAddons(PythonPackage):
    """New functionality not available in core TensorFlow"""

    homepage = "https://github.com/tensorflow/addons"
    url = "https://github.com/tensorflow/addons/archive/refs/tags/v0.19.0.tar.gz"

    version("0.19.0", sha256="6e1c40f03c9a35453a26eacbf36700f9666882418058a2f0d81aaa939135262f")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.7:", type=("build", "link", "run"))

    depends_on("py-typeguard@2.7:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-tensorflow@2.10.0", type=("build", "run"))
