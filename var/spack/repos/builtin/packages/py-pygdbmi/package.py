# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygdbmi(PythonPackage):
    """Parse gdb machine interface output with Python"""

    homepage = "https://github.com/cs01/pygdbmi"
    pypi = "pygdbmi/pygdbmi-0.8.2.0.tar.gz"

    license("MIT")

    version(
        "0.9.0.3",
        sha256="8fd98dd2e72d82667a4aa3cc34aedf951fe0e8f7e257cbdfc8e0fb7da250dc75",
        url="https://pypi.org/packages/da/cf/50ab83925820b3575c66b4668e4a307dfd668027df66830269ae027e5e32/pygdbmi-0.9.0.3-py3-none-any.whl",
    )
