# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class PyPydv(PythonPackage):
    """PyDV is a 1D graphics and data analysis tool, heavily based on the ULTRA plotting tool."""

    homepage = "https://github.com/griffin28/PyDV"
    # url = "https://github.com/griffin28/PyDV/archive/pydv-3.1.15.tar.gz"
    pypi = "llnl-pydv/llnl_pydv-3.1.15.tar.gz"
    git = "https://github.com/griffin28/PyDV"
    tags = ["pydv-3.1.15"]

    # notify when the package is updated
    maintainers("sbeljurf")

    # git branches
    version("master", branch="master")

    # pypi releases
    version("3.1.15", sha256="a47bae3aa5d0872674292bc87270b09885d7ccee8b6fbec72193371ba2599a04", preferred=True)

    depends_on("py-setuptools", type="build")
    depends_on("py-cycler", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyside", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))