# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRise(PythonPackage):
    """Reveal.js - Jupyter/IPython Slideshow Extension"""

    homepage = "https://rise.readthedocs.io/"
    pypi = "rise/rise-5.6.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.6.1",
        sha256="e9637ee5499ad7801474da53a2c830350a44b2192c2f113594e4426190e55ad4",
        url="https://pypi.org/packages/5c/f4/c226756f3e238a6109aba848ae7e1c96e5b3ed13bbd2916c5f0c6c207fe4/rise-5.6.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@5.4:")
        depends_on("py-notebook@5.5.0:", when="@5.3:5.6")
