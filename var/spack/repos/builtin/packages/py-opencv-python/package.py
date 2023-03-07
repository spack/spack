# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class PyOpencvPython(PythonPackage):
    """Pre-built CPU-only OpenCV packages for Python."""

    homepage = "https://pypi.org/project/opencv-python"
    pypi = "opencv-python/opencv-python-4.6.0.66.tar.gz"

    version("4.7.0.72", sha256="3424794a711f33284581f3c1e4b071cfc827d02b99d6fd9a35391f517c453306")
    version("4.6.0.66", sha256="c5bfae41ad4031e66bb10ec4a0a2ffd3e514d092652781e8b1ac98d1b59f1158")

    depends_on("cmake@3.1:", type="build")
    depends_on("py-wheel@0.37.0:", type="build")
    depends_on("py-scikit-build@0.13.2:", type="build")
    depends_on("py-setuptools@59.2.0", type="build")

    if platform.machine() in ["aarch64", "arm64"]:
        aarch = "arm64"
    else:
        aarch = platform.machine()

    if aarch != "arm64":
        depends_on("py-numpy@1.14.5", when="@4.6.0.66 ^python@3.7")
        depends_on("py-numpy@1.17.0", when="@4.7.0.72 ^python@3.7")
        depends_on("py-numpy@1.17.3", when="^python@3.8")
        depends_on("py-numpy@1.19.3", when="^python@3.9")
    elif aarch == "arm64":
        depends_on("py-numpy@1.19.3", when="^python@:3.9 platform=linux")
        depends_on("py-numpy@1.21.0", when="^python@:3.9 platform=darwin")

    for supported_platform in ["cray", "linux", "windows"]:
        depends_on("py-numpy@1.21.2", when=f"^python@3.10 platform={supported_platform}")
    depends_on("py-numpy@1.21.4", when="@4.7.0.72 ^python@3.10 platform=darwin")
    depends_on("py-numpy@1.21.2", when="@4.6.0.66 ^python@3.10:")
    depends_on("py-numpy@1.22.0", when="@4.7.0.72 ^python@3.11:")
