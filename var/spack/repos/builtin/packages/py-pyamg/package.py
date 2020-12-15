# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install py-pyamg
#
# You can edit this file again by typing:
#
#     spack edit py-pyamg
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPyamg(PythonPackage):
  """PyAMG is a library of Algebraic Multigrid (AMG) solvers with
  a convenient Python interface."""

  homepage = "https://github.com/pyamg/pyamg"
  url      = "https://github.com/pyamg/pyamg/archive/v4.0.0.zip"

# A list of GitHub accounts to notify when the package is updated.
  maintainers = []

  version('4.0.0', sha256 = "015d5e706e6e54d3de82e05fdb173c30d8b27cb8a117ab584cd62ad41d9ea042")

# Dependencies. A generic python dependency is added implicity by the
# PythonPackage class.
  depends_on("py-setuptools", type = "build")
  depends_on("py-numpy", type = ("build", "run"))
  depends_on("py-scipy", type = ("build", "run"))

#   def build_args(self, spec, prefix):
# # Add arguments other than --prefix.  If not needed delete this
# # function
#     args = []
#     return args
