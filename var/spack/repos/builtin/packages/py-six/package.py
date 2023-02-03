# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySix(Package, PythonExtension):
    """Python 2 and 3 compatibility utilities."""

    homepage = "https://github.com/benjaminp/six"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py2.py3/s/six/six-1.16.0-py2.py3-none-any.whl"
    list_url = "https://pypi.org/simple/six/"

    version(
        "1.16.0",
        sha256="8abb2f1d86890a2dfb989f9a77cfcfd3e47c2a354b01111771326f8aa26e0254",
        expand=False,
    )
    version(
        "1.15.0",
        sha256="8b74bedcbbbaca38ff6d7491d76f2b06b3592611af620f8426e82dddb04a5ced",
        expand=False,
    )
    version(
        "1.14.0",
        sha256="8f3cd2e254d8f793e7f3d6d9df77b92252b52637291d0f0da013c76ea2724b6c",
        expand=False,
    )
    version(
        "1.12.0",
        sha256="3350809f0555b11f552448330d0b52d5f24c91a322ea4a15ef22629740f3761c",
        expand=False,
    )
    version(
        "1.11.0",
        sha256="832dc0e10feb1aa2c68dcc57dbb658f1c7e65b9b61af69048abc87a2db00a0eb",
        expand=False,
    )
    version(
        "1.10.0",
        sha256="0ff78c403d9bccf5a425a6d31a12aa6b47f1c21ca4dc2573a7e2f32a97335eb1",
        expand=False,
    )
    version(
        "1.9.0",
        sha256="418a93c397a7edab23e5588dbc067ac74a723edb3d541bd4936f79476e7645da",
        expand=False,
    )
    version(
        "1.8.0",
        sha256="facfe0c7cceafd49e8f7e472111294566605fdfddc23011da06cc3a4601c9f7d",
        expand=False,
    )

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
