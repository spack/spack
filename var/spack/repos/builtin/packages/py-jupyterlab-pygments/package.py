# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlabPygments(PythonPackage):
    """Pygments theme using JupyterLab CSS variables."""

    homepage = "https://jupyter.org/"
    url = "https://files.pythonhosted.org/packages/py2.py3/j/jupyterlab-pygments/jupyterlab_pygments-0.2.2-py2.py3-none-any.whl"
    # We use wheels because in @0.2.2: there is a cyclic dependency between
    # py-nbconvert and py-jupyter-server:
    # py-nbconvert -> py-jupyterlab-pygments -> py-jupyterlab ->
    # -> py-jupyter-server -> py-nbconvert
    # Reported here: https://github.com/jupyterlab/jupyterlab_pygments/issues/23

    version(
        "0.2.2",
        sha256="2405800db07c9f770863bcf8049a529c3dd4d3e28536638bd7c1c01d2748309f",
        url="https://pypi.org/packages/c0/7e/c3d1df3ae9b41686e664051daedbd70eea2e1d2bd9d9c33e7e1455bc9f96/jupyterlab_pygments-0.2.2-py2.py3-none-any.whl",
    )
    version(
        "0.1.2",
        sha256="abfb880fd1561987efaefcb2d2ac75145d2a5d0139b1876d5be806e32f630008",
        url="https://pypi.org/packages/a8/6f/c34288766797193b512c6508f5994b830fb06134fdc4ca8214daba0aa443/jupyterlab_pygments-0.1.2-py2.py3-none-any.whl",
    )
    version(
        "0.1.1",
        sha256="c9535e5999f29bff90bd0fa423717dcaf247b71fad505d66b17d3217e9021fc5",
        url="https://pypi.org/packages/1f/4c/905faabb03f56ba92b1b9049436afead02bc09aae7e8f0d1107ebb46b151/jupyterlab_pygments-0.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.2")
        depends_on("py-pygments@2.4.1:", when="@:0.1")
