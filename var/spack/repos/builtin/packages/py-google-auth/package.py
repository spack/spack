# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleAuth(PythonPackage):
    """This library simplifies using Google's various server-to-server
    authentication mechanisms to access Google APIs."""

    homepage = "https://github.com/GoogleCloudPlatform/google-auth-library-python"
    pypi = "google-auth/google-auth-1.6.3.tar.gz"

    version("2.16.2", sha256="07e14f34ec288e3f33e00e2e3cc40c8942aa5d4ceac06256a28cd8e786591420")
    version("2.11.0", sha256="ed65ecf9f681832298e29328e1ef0a3676e3732b2e56f41532d45f70a22de0fb")
    version("2.3.2", sha256="2dc5218ee1192f9d67147cece18f47a929a9ef746cb69c50ab5ff5cfc983647b")
    version("1.6.3", sha256="0f7c6a64927d34c1a474da92cfc59e552a5d3b940d3266606c6a28b72888b9e4")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-cachetools@2:5", when="@2.11:", type=("build", "run"))
    depends_on("py-cachetools@2:4", when="@2.3", type=("build", "run"))
    depends_on("py-cachetools@2:", type=("build", "run"))
    depends_on("py-pyasn1-modules@0.2.1:", type=("build", "run"))
    depends_on("py-rsa@3.1.4:4", when="@2.3:", type=("build", "run"))
    depends_on("py-rsa@3.1.4:", type=("build", "run"))
    depends_on("py-six@1.9:", type=("build", "run"))
