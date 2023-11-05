# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIniconfig(PythonPackage):
    """
    iniconfig: brain-dead simple parsing of ini files
    """

    pypi = "iniconfig/iniconfig-1.1.1.tar.gz"

    version("2.0.0", sha256="2d91e135bf72d31a410b17c16da610a82cb55f6b0477d1a902134b24a455b8b3")
    version("1.1.1", sha256="bc3af051d7d14b2ee5ef9969666def0cd1a000e121eaea580d4a313df4b37f32")

    depends_on("py-hatchling", type="build", when="@2")
    depends_on("py-hatch-vcs", type="build", when="@2")
    depends_on("py-setuptools@41.2:", type="build", when="@1")
    depends_on("py-setuptools-scm@4:", type="build", when="@1")
