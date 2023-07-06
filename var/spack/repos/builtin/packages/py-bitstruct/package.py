# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
#     spack install py-bitstruct
#
# You can edit this file again by typing:
#
#     spack edit py-bitstruct
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyBitstruct(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/eerimoq/bitstruct"
    pypi = "bitstruct/bitstruct-8.17.0.tar.gz"

    maintainers("DaxLynch")

    version("8.17.0", sha256="eb94b40e4218a23aa8f90406b836a9e6ed83e48b8d112ce3f96408463bd1b874")

    depends_on("py-setuptools", type="build")

