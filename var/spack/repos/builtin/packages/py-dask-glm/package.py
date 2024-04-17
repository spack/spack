# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskGlm(PythonPackage):
    """Dask-glm is a library for fitting Generalized Linear Models on
    large datasets."""

    homepage = "https://dask-glm.readthedocs.io/en/latest/"
    pypi = "dask-glm/dask-glm-0.2.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.2.0",
        sha256="a116c36a830cc20660c0815c4c8d67239814931952e8695d784604cb4839ea51",
        url="https://pypi.org/packages/cb/ee/36c6e0e7b51e08406e5c3bb036f35adb77bd0a89335437b2e6f03c948f1a/dask_glm-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-cloudpickle@0.2.2:")
        depends_on("py-dask+array")
        depends_on("py-multipledispatch@0.4.9:")
        depends_on("py-scikit-learn@0.18:")
        depends_on("py-scipy@0.18.1:")
