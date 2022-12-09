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
#     spack install py-tzdata
#
# You can edit this file again by typing:
#
#     spack edit py-tzdata
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyTzdata(PythonPackage):
    """tzdata: Python package providing IANA time zone data"""

    homepage = "https://github.com/python/tzdata"

    url = "https://github.com/python/tzdata/archive/refs/tags/2022.7.tar.gz"
    git = "https://github.com/python/tzdata.git"

    maintainers = ["samcom12"]

    version("master", branch='master')

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

