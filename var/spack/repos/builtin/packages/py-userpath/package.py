# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUserpath(PythonPackage):
    """Cross-platform tool for adding locations to the user PATH."""

    homepage = "https://github.com/ofek/userpath"
    pypi = "userpath/userpath-1.8.0.tar.gz"

    license("MIT")

    version("1.8.0", sha256="04233d2fcfe5cff911c1e4fb7189755640e1524ff87a4b82ab9d6b875fee5787")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-hatchling", type="build")

    depends_on("py-click", type=("build", "run"))
