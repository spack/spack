# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyserial(PythonPackage):
    """Python Serial Port Extension"""

    homepage = "https://github.com/pyserial/pyserial"
    pypi = "pyserial/pyserial-3.1.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.1.1",
        sha256="b4fcd6a7d329c844781df80fb06a4a9e21f3ac5623a687a975cbce8a8e4a82d2",
        url="https://pypi.org/packages/49/db/5704dfc92d9a35f43d10744b0e661eeb1cbddc3bf8bd704592d653d23d86/pyserial-3.1.1-py2.py3-none-any.whl",
    )
