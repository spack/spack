# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorclass(PythonPackage):
    """Colorful worry-free console applications for Linux, Mac OS X, and Windows."""

    homepage = "https://github.com/Robpol86/colorclass"
    pypi = "colorclass/colorclass-2.2.2.tar.gz"

    version("2.2.2", sha256="6d4fe287766166a98ca7bc6f6312daf04a0481b1eda43e7173484051c0ab4366")
    version("2.2.1", sha256="f8435bff93eb1f77c41f8363f1ff8a8bb1b1fe1e459eb6482a3542a4018b5f31")
    version("2.2.0", sha256="b05c2a348dfc1aff2d502527d78a5b7b7e2f85da94a96c5081210d8e9ee8e18b")

    depends_on("python@3.3.0:")
    depends_on("py-poetry@0.12:", type="build")
    depends_on("py-docopt", type=("build", "run"))
