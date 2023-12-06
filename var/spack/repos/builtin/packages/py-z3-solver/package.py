# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-z3-solver
#
# You can edit this file again by typing:
#
#     spack edit py-z3-solver
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------
from spack.package import *


class PyZ3Solver(PythonPackage):
    """Z3 is a theorem prover from Microsoft Research. It is licensed under the MIT license."""

    homepage = "https://github.com/Z3Prover/z3"
    pypi = "z3-solver/z3-solver-4.12.3.0.tar.gz"

    license("MIT")

    version("4.12.3.0", sha256="b6719daf9676711a8f1c708af0ea185578b0f22a3cb9bf9a55735e21691dc38d")

    depends_on("py-setuptools@46.4:", type="build")
    depends_on("cmake", type="build")
