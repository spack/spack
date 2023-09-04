# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnsimarkup(PythonPackage):
    """Produce colored terminal text with an xml-like markup."""

    homepage = "https://github.com/gvalkov/python-ansimarkup"
    pypi = "ansimarkup/ansimarkup-1.5.0.tar.gz"

    maintainers("LydDeb")

    version("1.5.0", sha256="96c65d75bbed07d3dcbda8dbede8c2252c984f90d0ca07434b88a6bbf345fad3")

    depends_on("python@2.7,3.3:3.9", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-colorama", type=("build", "run"))
