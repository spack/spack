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
    url = "https://files.pythonhosted.org/packages/f7/7e/629ddbe63164f71bf2b03e151a69bfbf439692652432af4b2a78f21b0a18/utm-0.7.0.tar.gz"

    maintainers("samcom12")

    version("0.7.0", sha256="3c9a3650e98bb6eecec535418d0dfd4db8f88c8ceaca112a0ff0787e116566e2")

    # added implicity by the PythonPackage base class.
    depends_on("python@3:", type=("build", "run"))
    depends_on("py-pytest", type="build")
    depends_on("py-numpy", type=("build", "run", "link"))
