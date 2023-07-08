# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt5Sip(PythonPackage):
    """The sip module support for PyQt5."""

    homepage = "https://www.riverbankcomputing.com/software/sip/"
    pypi = "PyQt5-sip/PyQt5_sip-12.9.0.tar.gz"

    version("12.11.0", sha256="b4710fd85b57edef716cc55fae45bfd5bfac6fc7ba91036f1dcc3f331ca0eb39")
    version("12.9.0", sha256="d3e4489d7c2b0ece9d203ae66e573939f7f60d4d29e089c9f11daa17cfeaae32")

    depends_on("py-setuptools@30.3:", type="build")
