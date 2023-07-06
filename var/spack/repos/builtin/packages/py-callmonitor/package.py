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
#     spack install py-callmonitor
#
# You can edit this file again by typing:
#
#     spack edit py-callmonitor
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyCallmonitor(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/JBlaschke/call-monitor"
    pypi = "callmonitor/callmonitor-0.3.7.tar.gz"

    maintainers("DaxLynch")

    version("0.3.7", sha256="11bacfe5940c3f6aff223e8e761b033d540542b4d738f7fef38cd923b3be0cbc")

    depends_on("py-setuptools", type="build")

