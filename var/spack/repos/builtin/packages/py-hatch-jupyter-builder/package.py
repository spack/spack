# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchJupyterBuilder(PythonPackage):
    """A hatch plugin to help build Jupyter packages."""

    homepage = "https://github.com/jupyterlab/hatch-jupyter-builder"
    pypi = "hatch_jupyter_builder/hatch_jupyter_builder-0.8.3.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.8.3",
        sha256="d9e5666ee61877f31d49a2e0faafb034816c9813de65997baa691bd734092e54",
        url="https://pypi.org/packages/11/3f/be50e0763e2dc2b354d807caf4fec9b6f6b30f70926b2568e820c050ef82/hatch_jupyter_builder-0.8.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.8.2:")
        depends_on("py-hatchling@1.5:", when="@0.8.2:0.8")
