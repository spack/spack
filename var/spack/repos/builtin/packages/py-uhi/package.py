# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUhi(PythonPackage):
    """Unified Histogram Interface:
    tools to help library authors work with histograms"""

    homepage = "https://github.com/Scikit-HEP/uhi"
    pypi = "uhi/uhi-0.3.0.tar.gz"

    version("0.3.1", sha256="6f1ebcadd1d0628337a30b012184325618047abc01c3539538b1655c69101d91")
    version("0.3.0", sha256="3f441bfa89fae11aa762ae1ef1b1b454362d228e9084477773ffb82d6e9f5d2c")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-numpy@1.13.3:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7:", type=("build", "run"), when="^python@:3.7")
    depends_on("py-poetry-core@1:", when="@:0.3.0", type="build")
    depends_on("py-flit-core@3.2:", when="@0.3.1:", type="build")
