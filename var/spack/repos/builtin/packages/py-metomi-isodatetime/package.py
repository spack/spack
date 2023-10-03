# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetomiIsodatetime(PythonPackage):
    """Python ISO 8601 date time parser and data model/manipulation utilities."""

    homepage = "https://github.com/metomi/isodatetime"
    pypi = "metomi-isodatetime/metomi-isodatetime-1!3.0.0.tar.gz"

    maintainers("LydDeb")

    version("3.0.0", sha256="2141e8aaa526ea7f7f1cb883e6c8ed83ffdab73269658d84d0624f63a6e1357e")

    depends_on("py-setuptools", type="build")
