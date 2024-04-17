# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGoogle(PythonPackage):
    """Python bindings to the Google search engine."""

    homepage = "https://breakingcode.wordpress.com/"
    pypi = "google/google-3.0.0.tar.gz"

    version(
        "3.0.0",
        sha256="889cf695f84e4ae2c55fbc0cfdaf4c1e729417fa52ab1db0485202ba173e4935",
        url="https://pypi.org/packages/ac/35/17c9141c4ae21e9a29a43acdfd848e3e468a810517f862cad07977bf8fe9/google-3.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-beautifulsoup4", when="@:1,2.0.3:")
