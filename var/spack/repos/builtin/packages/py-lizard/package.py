# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLizard(PythonPackage):
    """A code analyzer without caring the C/C++ header files.
    It works with Java, C/C++, JavaScript, Python, Ruby,
    Swift, Objective C. Metrics includes cyclomatic
    complexity number etc."""

    homepage = "http://www.lizard.ws/"
    pypi = "lizard/lizard-1.17.9.tar.gz"

    license("MIT")

    version(
        "1.17.10",
        sha256="686748cc003de54d3e37f84b6cbbdd975be41a2094f0a779cb7fef65e70fc53e",
        url="https://pypi.org/packages/ef/4b/557cbe718f0550de5656f7480600989ddfc0279db15e90d9cdc38cb8e61d/lizard-1.17.10-py2.py3-none-any.whl",
    )
    version(
        "1.17.9",
        sha256="3a5c429321e67d4a1970adb30ce8c6aebf4688c275b2589d89b4bbd6ed3d40a9",
        url="https://pypi.org/packages/4d/2e/ef0a4cc393164d24e5b2784850ed92dbd27999ab51244cd38a62dac48ff8/lizard-1.17.9-py2.py3-none-any.whl",
    )
