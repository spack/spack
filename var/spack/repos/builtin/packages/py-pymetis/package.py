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
#     spack install py-pymetis
#
# You can edit this file again by typing:
#
#     spack edit py-pymetis
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyPymetis(PythonPackage):
    """PyMetis is a Python wrapper for the Metis graph partititioning software by George Karypis, Vipin Kumar and others. It includes version 5.1.0 of Metis and wraps it using the Pybind11 wrapper generator library. """

    homepage = "https://mathema.tician.de/software/pymetis/"
    url = "https://files.pythonhosted.org/packages/5c/c2/545ba0032bb8c32ec6de7f2de92f301835a2002f77ff09a6471a7610bc36/PyMetis-2023.1.tar.gz"

    maintainers("samcom12")

    version("2023.1", sha256="779eaaaa3ddcf780ec6a4678e6e4690aff9a658a304bd4c4efb8abdd6bd0b71e")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-pybind11", type=("build", "test", "run"))
    depends_on("py-numpy", type=("build", "test", "run"))
    depends_on("py-meshpy", type=("build", "test", "run"))
