# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyPyspy(PythonPackage):
    """py-spy is a sampling profiler for Python programs."""

    homepage = "https://github.com/benfred/py-spy"
    url = "https://files.pythonhosted.org/packages/51/70/e8bfeeac2c57f3af9988ca6d6d12cff3a9a1394e0d9a2c63f08555c0552f/py_spy-0.1.0-py2.py3-none-manylinux1_x86_64.whl"
    git = "https://github.com/benfred/py-spy.git"

    if sys.platform == "darwin":
        version(
            "0.3.14",
            sha256="fe7efe6c91f723442259d428bf1f9ddb9c1679828866b353d539345ca40d9dd2",
            expand=False,
            url="https://files.pythonhosted.org/packages/4c/f3/ace9005f101cb7d41bd69081ea4d095950a31bb6df8a26cf142928e7658f/py_spy-0.3.14-py2.py3-none-macosx_10_9_x86_64.macosx_11_0_arm64.macosx_10_9_universal2.whl",
        )
    elif sys.platform.startswith("linux"):
        version(
            "0.3.14",
            sha256="f59b0b52e56ba9566305236375e6fc68888261d0d36b5addbe3cf85affbefc0e",
            expand=False,
            url="https://files.pythonhosted.org/packages/c2/d2/082de8db2285a652a00a39f2bcffaaf0b0c9c378f4830bb5983d2600b2dd/py_spy-0.3.14-py2.py3-none-manylinux_2_5_x86_64.manylinux1_x86_64.whl",
        )

    conflicts("target=ppc64:", msg="py-pyspy is only available for x86_64")
    conflicts("target=ppc64le:", msg="py-pyspy is only available for x86_64")
    conflicts("target=aarch64:", msg="py-pyspy is only available for x86_64")

    depends_on("python", type=("build", "run"))
