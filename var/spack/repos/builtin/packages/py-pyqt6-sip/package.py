# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt6Sip(PythonPackage):
    """The sip module support for PyQt6."""

    homepage = "https://www.riverbankcomputing.com/software/sip/"
    pypi = "PyQt6-sip/PyQt6_sip-13.4.0.tar.gz"

    version("13.4.0", sha256="6d87a3ee5872d7511b76957d68a32109352caf3b7a42a01d9ee20032b350d979")

    depends_on("py-setuptools@30.3:", type="build")
