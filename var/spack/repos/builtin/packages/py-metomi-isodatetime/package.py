# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetomiIsodatetime(PythonPackage):
    """Python ISO 8601 date time parser and data model/manipulation utilities."""

    homepage = "https://github.com/metomi/isodatetime"
    url = "https://github.com/metomi/isodatetime/archive/refs/tags/3.0.0.tar.gz"

    maintainers("LydDeb")

    version("3.0.0", sha256="ecf592e10ceef68ff31df79b909f919383752b57308299f6fc8b8d2ce8471d15")

    depends_on("py-setuptools", type="build")
