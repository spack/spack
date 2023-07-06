# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQmtest(PythonPackage):
    """A general purpose testing framework"""

    homepage = "https://github.com/MentorEmbedded/qmtest"
    url = "https://github.com/MentorEmbedded/qmtest/archive/refs/tags/2.4.1.tar.gz"

    maintainers("haralmha")

    version("2.4.1", sha256="098f705aea9c8f7f5b6b5fe131974cee33b50cad3e13977e39708f306ce9ac91")

    # Patch to fix python 3.10 and above compatibility
    patch("wininst.patch", when="@2.4.1^python@3.10:")

    depends_on("python@2.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
