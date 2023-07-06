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
#     spack install py-nvtx
#
# You can edit this file again by typing:
#
#     spack edit py-nvtx
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyNvtx(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/JBlaschke/PyNVTX/tree/master"
    pypi = "PyNVTX/PyNVTX-0.3.3.tar.gz"

    maintainers("DaxLynch")

    version("0.3.3", sha256="8877b2d90bbf9d279d517a80a8f35a0a0a8179ebabf0729e806798a84bee6c72")

    depends_on("py-setuptools", type="build")
    depends_on("py-pybind11", type=("build", "run"))

