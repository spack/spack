# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbclassic(PythonPackage):
    """Jupyter Notebook as a Jupyter Server Extension."""

    homepage = "https://github.com/jupyterlab/nbclassic"
    pypi = "nbclassic/nbclassic-0.3.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.0.0",
        sha256="f99e4769b4750076cd4235c044b61232110733322384a94a63791d2e7beacc66",
        url="https://pypi.org/packages/84/ae/eaa71c0ed64e8ddc426a4c902e83d31c4925e9d3418d6b240dd5752b6e71/nbclassic-1.0.0-py3-none-any.whl",
    )
    version(
        "0.4.8",
        sha256="cbf05df5842b420d5cece0143462380ea9d308ff57c2dc0eb4d6e035b18fbfb3",
        url="https://pypi.org/packages/a6/85/2a240df7326b7311ebd926c12d7df5394aef2f9f76ffbb294079cc43960e/nbclassic-0.4.8-py3-none-any.whl",
    )
    version(
        "0.3.5",
        sha256="012d18efb4e24fe9af598add0dcaa621c1f8afbbbabb942fb583dd7fbb247fc8",
        url="https://pypi.org/packages/6f/45/21eaa314a406e2ba5c000ad755d1153b3269d338800674b5ff5f62f1f0fb/nbclassic-0.3.5-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="a7437c90a0bffcce172a4540cc53e140ea5987280c87c31a0cfa6e5d315eb907",
        url="https://pypi.org/packages/11/68/217ab6d4e4676dcfa4e855bb435469164a361a58e1856872cb06277f14b5/nbclassic-0.3.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.3.6:")
        depends_on("py-argon2-cffi", when="@0.4:")
        depends_on("py-ipykernel", when="@0.4:")
        depends_on("py-ipython-genutils", when="@0.4:")
        depends_on("py-jinja2", when="@0.4:")
        depends_on("py-jupyter-client@6.1.1:", when="@0.4:")
        depends_on("py-jupyter-core@4.6.1:", when="@0.4:")
        depends_on("py-jupyter-server@1.8:", when="@0.3.7:")
        depends_on("py-jupyter-server@1.8:1", when="@0.3.1:0.3.6")
        depends_on("py-nbconvert@5.0.0:", when="@0.4:")
        depends_on("py-nbformat", when="@0.4:")
        depends_on("py-nest-asyncio@1.5:", when="@0.4:")
        depends_on("py-notebook@:6", when="@:0.2.0,0.2.2:0.3")
        depends_on("py-notebook-shim@0.2.3:", when="@0.5.6:")
        depends_on("py-notebook-shim@0.1:", when="@0.3.6:0.5.5")
        depends_on("py-prometheus-client", when="@0.4:")
        depends_on("py-pyzmq@17.0.0:", when="@0.4:")
        depends_on("py-send2trash@1.8:", when="@0.4:")
        depends_on("py-terminado@0.8.3:", when="@0.4:")
        depends_on("py-tornado@6.1:", when="@0.4:")
        depends_on("py-traitlets@4.2.1:", when="@0.4:")

    # version requirement for py-jupyter-server comes from pyproject.toml

    # Historical dependencies
