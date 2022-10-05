# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDistlib(PythonPackage):
    """Distribution utilities"""

    homepage = "https://bitbucket.org/pypa/distlib"
    pypi = "distlib/distlib-0.3.6.tar.gz"

    version("0.3.6", sha256="14bad2d9b04d3a36127ac97f30b12a19268f211063d8f8ee4f47108896e11b46")
    version(
        "0.3.4",
        sha256="e4b58818180336dc9c529bfb9a0b58728ffc09ad92027a3f30b7cd91e3458579",
        url="https://files.pythonhosted.org/packages/85/01/88529c93e41607f1a78c1e4b346b24c74ee43d2f41cfe33ecd2e20e0c7e3/distlib-0.3.4.zip",
    )
    version(
        "0.3.3",
        sha256="d982d0751ff6eaaab5e2ec8e691d949ee80eddf01a62eaa96ddb11531fe16b05",
        url="https://files.pythonhosted.org/packages/56/ed/9c876a62efda9901863e2cc8825a13a7fcbda75b4b498103a4286ab1653b/distlib-0.3.3.zip",
    )

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
