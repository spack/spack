# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxRemovedIn(PythonPackage):
    """versionremoved and removed-in directives for Sphinx."""

    homepage = "https://github.com/MrSenko/sphinx-removed-in"
    pypi = "sphinx-removed-in/sphinx-removed-in-0.2.1.tar.gz"

    maintainers("LydDeb")

    version(
        "0.2.1",
        sha256="434b1a1c28b12021de4c84fc2fbb7168fdf1f56a410a42bf8d0af938d0855ad1",
        url="https://pypi.org/packages/c0/2e/a69508232549ca59cdb34494232f33684558d121f4bcca5ade5c5221dc19/sphinx_removed_in-0.2.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-sphinx", when="@0.2:")
