# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------
from spack.package import *


class PyRequirementsParser(PythonPackage):
    """This is a small Python module for parsing Pip requirement files."""

    homepage = "https://github.com/madpah/requirements-parser/tree/master"
    url = "https://files.pythonhosted.org/packages/c2/f9/76106e710015f0f8da37bff8db378ced99ae2553cc4b1cffb0aef87dc4ac/requirements-parser-0.5.0.tar.gz"

    maintainers("DaxLynch")

    depends_on("py-poetry-core", type="build")

    version("0.5.0", sha256="3336f3a3ae23e06d3f0f88595e4052396e3adf91688787f637e5d2ca1a904069")
