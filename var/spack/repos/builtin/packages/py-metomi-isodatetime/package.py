# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetomiIsodatetime(PythonPackage):
    """Python ISO 8601 date time parser and data model/manipulation utilities."""

    homepage = "https://github.com/metomi/isodatetime"
    # NOTE: spack checksum does not yet work for epoch versions
    pypi = "metomi-isodatetime/metomi-isodatetime-1!3.0.0.tar.gz"

    maintainers("LydDeb")

    version(
        "1.3.1.0",
        sha256="837880717817d0325703b9b3ce94093fc92fc7ac18cd14f9fe389f2d21266407",
        url="https://pypi.org/packages/8b/5f/8446ce923b5aa995e5fbd75af4f00cc6666fd16883add8c9644b4f89ef04/metomi_isodatetime-1!3.1.0-py3-none-any.whl",
    )
    version(
        "1.3.0.0",
        sha256="29dfebfd51d344a7692d42a765756cdcbd22f7c615375cd9e86b7be64810db69",
        url="https://pypi.org/packages/6b/bb/7651139d2039d17a3a47d0181fccbd04436db67ceac1243ef25cdb2e3747/metomi_isodatetime-1!3.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.3.1:")
