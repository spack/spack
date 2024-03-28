# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCffconvert(PythonPackage):
    """Command line program to validate and convert CITATION.cff files."""

    homepage = "https://github.com/citation-file-format/cff-converter-python"
    pypi = "cffconvert/cffconvert-2.0.0.tar.gz"

    license("Apache-2.0")

    version(
        "2.0.0",
        sha256="573c825e4e16173d99396dc956bd22ff5d4f84215cc16b6ab05299124f5373bb",
        url="https://pypi.org/packages/42/ae/28c3d933b4343f61cc5d63748b53746e5d73b1f66c88e7a93477f22b8909/cffconvert-2.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-click@7:", when="@2:")
        depends_on("py-jsonschema@3.0.0:3", when="@2:")
        depends_on("py-pykwalify@1.6:", when="@2:")
        depends_on("py-requests@2.20:", when="@2:")
        depends_on("py-ruamel-yaml@0.16:", when="@2:")
