# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLibsbml(PythonPackage):
    """LibSBML is a library for reading, writing and manipulating the Systems Biology
    Markup Language (SBML)."""

    homepage = "https://sbml.org/"
    url = "https://github.com/sbmlteam/python-libsbml"
    git = "https://github.com/sbmlteam/python-libsbml.git"

    version("5.19.5", tag="v5.19.5", submodules=True)

    depends_on("py-setuptools", type="build")

    depends_on("swig@2:", type="build")
    depends_on("cmake", type="build")
    depends_on("zlib")
    depends_on("bzip2")
    depends_on("libxml2")
