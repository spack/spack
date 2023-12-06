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
#     spack install py-pywin32
#
# You can edit this file again by typing:
#
#     spack edit py-pywin32
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyPywin32(PythonPackage):
    """Python for Window Extensions."""

    homepage = "https://github.com/mhammond/pywin32"
    url = "https://github.com/mhammond/pywin32/archive/refs/tags/b306.tar.gz"

    license("UNKNOWN")

    version("306", sha256="16e5ad3efbbf997080f67c3010bd4eb0067d499bbade9be1b240b7e85325c167")

    depends_on("py-setuptools", type="build")
