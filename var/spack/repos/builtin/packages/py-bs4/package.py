# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBs4(PythonPackage):
    """Screen-scraping library"""

    homepage = "https://pypi.python.org/pypi/beautifulsoup4"
    pypi = "bs4/bs4-0.0.1.tar.gz"

    maintainers("LydDeb")

    version("0.0.1", sha256="36ecea1fd7cc5c0c6e4a1ff075df26d50da647b75376626cc186e2212886dd3a")

    depends_on("py-setuptools", type="build")
    depends_on("py-beautifulsoup4", type=("build", "run"))
