# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterPackaging10(PythonPackage):
    """Jupyter Packaging Utilities, version 10."""

    # TODO: This package only exists because different packages in the Jupyter ecosystem
    # require different versions of jupyter_packaging. Once the concretizer is capable
    # of concretizing build dependencies separately, this package should be removed.

    homepage = "https://github.com/jupyter/jupyter-packaging"
    pypi = "jupyter_packaging/jupyter-packaging-0.10.6.tar.gz"

    version("0.10.6", sha256="a8a2c90bf2e0cae83be63ccb0b7035032a1589f268cc08b1d479e37ce50fc940")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    # Upper limit due to https://github.com/jupyter/jupyter-packaging/issues/130
    depends_on("py-setuptools@46.4.0:60", type=("build", "run"))
