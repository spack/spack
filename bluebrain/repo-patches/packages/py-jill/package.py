# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJill(PythonPackage):
    """Julia Installer for Linux (and every other platform)"""

    homepage = "https://github.com/johnnychen94/jill.py"
    pypi = "jill/jill-0.11.1.tar.gz"

    maintainers("tristan0x")

    version("0.11.1", sha256="fbfac07da3892672d09c489cf3be5d31ae38ac22b68ea49b147dbe79e339021b")

    depends_on("py-setuptools", type="build")
    depends_on("py-poetry-core", type="build")

    depends_on("py-fire", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-python-gnupg", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-requests-futures", type=("build", "run"))
    depends_on("py-semantic-version", type=("build", "run"))
    depends_on("py-wget", type=("build", "run"))
