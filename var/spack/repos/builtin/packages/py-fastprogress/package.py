# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastprogress(PythonPackage):
    """A fast and simple progress bar for Jupyter Notebook and
    console. Created by Sylvain Gugger for fast.ai."""

    homepage = "https://github.com/fastai/fastprogress"
    pypi = "fastprogress/fastprogress-1.0.0.tar.gz"

    version(
        "1.0.0",
        sha256="474cd6a6e5b1c29a02383d709bf71f502477d0849bddc6ba5aa80b683f4ad16f",
        url="https://pypi.org/packages/eb/1f/c61b92d806fbd06ad75d08440efe7f2bd1006ba0b15d086debed49d93cdc/fastprogress-1.0.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-numpy", when="@1:1.0.1")
