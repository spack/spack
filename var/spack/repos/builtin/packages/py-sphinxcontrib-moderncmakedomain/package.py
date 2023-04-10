# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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
#     spack install py-sphinxcontrib-moderncmakedomain
#
# You can edit this file again by typing:
#
#     spack edit py-sphinxcontrib-moderncmakedomain
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PySphinxcontribModerncmakedomain(PythonPackage):
    """Sphinx Domain for Modern CMake."""

    homepage = "https://github.com/scikit-build/moderncmakedomain"
    pypi = "sphinxcontrib_moderncmakedomain/sphinxcontrib_moderncmakedomain-3.25.0.tar.gz"

    maintainers("greenc-FNAL", "gartung", "marcmengel", "vitodb")

    version("3.25.0", sha256="4138e4d3f60e5c4b3982caa10033693bfc1009cdd851766754d5990d9d1e992a")

    conflicts("python@:3.5")

    depends_on("py-hatchling", type="build")

    depends_on("py-sphinx", type=("build", "run"))
