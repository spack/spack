# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLibsbml(PythonPackage):
    """LibSBML is a library for reading, writing and manipulating the Systems Biology
    Markup Language (SBML)."""

    homepage = "https://sbml.org/"
    git = "https://github.com/sbmlteam/python-libsbml.git"
    pypi = "python-libsbml/python-libsbml-5.19.7.tar.gz"

    version("5.19.7", sha256="447b1fde7aceccd11a93dc9f589ffd9319ba854d7b7583f911259a8b0127ab7b")
    version("5.19.5", tag="v5.19.5", submodules=True)

    depends_on("py-setuptools", type="build")

    depends_on("swig", type="build")
    depends_on("cmake", type=("build", "run"))
