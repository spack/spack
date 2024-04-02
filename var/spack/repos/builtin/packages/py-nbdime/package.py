# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbdime(PythonPackage):
    """Diff and merge of Jupyter Notebooks"""

    homepage = "https://nbdime.readthedocs.io/"
    pypi = "nbdime/nbdime-3.1.1.tar.gz"

    version(
        "3.1.1",
        sha256="ea4ddf919e3035800ef8bd5552b814522207cb154ca7512565e4539a54c74dbf",
        url="https://pypi.org/packages/49/e2/aae3b46d8aa9994470454bfacb1c780196c1f53662656f32073ad90307a7/nbdime-3.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colorama")
        depends_on("py-gitpython@:2.1.3,2.1.7:")
        depends_on("py-jinja2@2.9:")
        depends_on("py-jupyter-server", when="@3:")
        depends_on("py-jupyter-server-mathjax@0.2.2:", when="@3.0.0:3,4.0.0-alpha1:")
        depends_on("py-nbformat")
        depends_on("py-pygments")
        depends_on("py-requests")
        depends_on("py-tornado")

    # From pyproject.toml
