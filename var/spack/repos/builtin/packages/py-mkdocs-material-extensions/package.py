# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocsMaterialExtensions(PythonPackage):
    """Markdown extension resources for MkDocs for Material."""

    homepage = "https://github.com/facelessuser/mkdocs-material-extensions"
    pypi = "mkdocs-material-extensions/mkdocs-material-extensions-1.0.3.tar.gz"

    license("MIT")

    version(
        "1.0.3",
        sha256="a82b70e533ce060b2a5d9eb2bc2e1be201cf61f901f93704b4acf6e3d5983a44",
        url="https://pypi.org/packages/cc/f5/cc42642eb7bb4f8df06c058ea9a7e45f3be141851845ee77ff8eeb16e86b/mkdocs_material_extensions-1.0.3-py3-none-any.whl",
    )
