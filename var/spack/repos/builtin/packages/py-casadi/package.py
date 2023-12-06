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
#     spack install casadi
#
# You can edit this file again by typing:
#
#     spack edit casadi
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------
from spack.package import *


class PyCasadi(PythonPackage):
    """CasADi -- framework for algorithmic differentiation and numeric optimization"""

    homepage = "casadi.org"
    pypi = "casadi/casadi-3.6.4.tar.gz"

    license("LGPL")

    version("3.6.4", sha256="affdca1a99c14580992cdf34d247754b7d851080b712c2922ad2e92442eeaa35")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type="run")
