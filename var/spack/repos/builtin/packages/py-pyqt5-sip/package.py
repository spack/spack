# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt5Sip(PythonPackage):
    """The sip module support for PyQt5."""

    homepage = "https://www.riverbankcomputing.com/software/sip/"
    pypi = "PyQt5-sip/PyQt5_sip-12.9.0.tar.gz"

    license("GPL-2.0-only")

    version("12.12.1", sha256="8fdc6e0148abd12d977a1d3828e7b79aae958e83c6cb5adae614916d888a6b10")
    version("12.9.0", sha256="d3e4489d7c2b0ece9d203ae66e573939f7f60d4d29e089c9f11daa17cfeaae32")

    depends_on("py-setuptools@30.3:", type="build")
