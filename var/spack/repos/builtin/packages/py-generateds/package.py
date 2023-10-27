# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGenerateds(PythonPackage):
    """Generate Python data structures and XML parser from Xschema."""

    homepage = "http://www.davekuhlman.org/generateDS.html"
    pypi = "generateDS/generateDS-2.41.4.tar.gz"

    maintainers("LydDeb")

    version("2.41.4", sha256="804592eef573fa514741528a0bf9998f0c57ee29960c87f54608011f1fc722ea")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-requests@2.21:", type=("build", "run"))
