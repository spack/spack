# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModin(PythonPackage):
    """Modin: Make your pandas code run faster by changing one line of code."""

    homepage = "https://github.com/modin-project/modin"
    pypi = "modin/modin-0.16.2.tar.gz"

    version("0.16.2", sha256="8e3f4cb478ae08dcc71b5a345781d57f29d6b95bc6ce1dc5c14d597a382f1354")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pandas@1.5.1", when="^python@3.8:", type=("build", "run"))
    depends_on("py-pandas@1.1.5", when="^python@:3.7", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-numpy@1.18.5:", type=("build", "run"))
    depends_on("py-fsspec", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
