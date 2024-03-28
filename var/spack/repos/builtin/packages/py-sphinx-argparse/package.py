# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxArgparse(PythonPackage):
    """Sphinx extension to automatically document argparse-based commands."""

    homepage = "https://pypi.org/project/sphinx-argparse"
    pypi = "sphinx-argparse/sphinx-argparse-0.3.1.tar.gz"

    maintainers("sethrj")

    license("MIT")

    version(
        "0.3.1",
        sha256="295ccae425874630b6a3b47254854027345d786bab2c3ffd5e9a0407bc6856b2",
        url="https://pypi.org/packages/d3/78/ac134e24feef6cffde66d3b67439d07624749dbaddd7fe7404b22f01f85b/sphinx_argparse-0.3.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-sphinx@1.2:", when="@0.3:")
