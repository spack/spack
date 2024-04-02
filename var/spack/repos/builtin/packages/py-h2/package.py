# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH2(PythonPackage):
    """HTTP/2 State-Machine based protocol implementation"""

    homepage = "https://github.com/python-hyper/hyper-h2"
    pypi = "h2/h2-4.0.0.tar.gz"

    license("MIT")

    version(
        "4.1.0",
        sha256="03a46bcf682256c95b5fd9e9a99c1323584c3eec6440d379b9903d709476bc6d",
        url="https://pypi.org/packages/2a/e5/db6d438da759efbb488c4f3fbdab7764492ff3c3f953132efa6b9f0e9e53/h2-4.1.0-py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="ac9e293a1990b339d5d71b19c5fe630e3dd4d768c620d1730d355485323f1b25",
        url="https://pypi.org/packages/bd/c2/5ffec707d0022208787908d9657f782ce35b653baa1e87abecf22a7cf513/h2-4.0.0-py3-none-any.whl",
    )
    version(
        "3.2.0",
        sha256="61e0f6601fa709f35cdb730863b4e5ec7ad449792add80d1410d4174ed139af5",
        url="https://pypi.org/packages/25/de/da019bcc539eeab02f6d45836f23858ac467f584bfec7a526ef200242afe/h2-3.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-hpack@4:", when="@4:")
        depends_on("py-hpack@3", when="@3.2:3")
        depends_on("py-hyperframe@6:", when="@4:")
        depends_on("py-hyperframe@5.2:5", when="@3.1:3")
