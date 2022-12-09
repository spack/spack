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
#     spack install py-utm
#
# You can edit this file again by typing:
#
#     spack edit py-utm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyUtm(PythonPackage):
    """Bidirectional UTM-WGS84 converter for python"""

    homepage = "https://github.com/Turbo87/utm"
    git = "https://github.com/Turbo87/utm.git"
    url = "https://github.com/Turbo87/utm/archive/refs/tags/v0.7.0.tar.gz"


    maintainers = ["jayashripawar"]

    version("master", branch='master')

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("py-pytest", type=("build", "run"))
    depends_on("py-setuptools", type="build")
