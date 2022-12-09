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
#     spack install py-zoneinfo
#
# You can edit this file again by typing:
#
#     spack edit py-zoneinfo
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyZoneinfo(PythonPackage):
    """This package was originally the reference implementation for
        PEP 615, which proposes support for the IANA time zone database
        in the standard library, and now serves as a backport to Python 3.6+ (including PyPy). """

    homepage = "https://github.com/pganssle/zoneinfo"

    url = "https://github.com/pganssle/zoneinfo/archive/refs/tags/0.2.1.tar.gz"
    git = "https://github.com/pganssle/zoneinfo.git"

    maintainers = ["samcom12"]


    version("master", brnach='master', preferred=True)
    version('0.2.1', sha256='21bc8918f30a8b6f5ce4effe7b30398cfe7d010066329704421247cecaf7f397')

    depends_on("python@3.10", type=("build", "run"))
    depends_on("py-setuptools", type="build")
