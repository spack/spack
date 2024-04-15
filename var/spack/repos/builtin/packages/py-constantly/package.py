# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConstantly(PythonPackage):
    """Symbolic constants in Python"""

    homepage = "https://github.com/twisted/constantly"
    pypi = "constantly/constantly-15.1.0.tar.gz"

    license("MIT")

    version(
        "15.1.0",
        sha256="dd2fa9d6b1a51a83f0d7dd76293d734046aa176e384bf6e33b7e44880eb37c5d",
        url="https://pypi.org/packages/b9/65/48c1909d0c0aeae6c10213340ce682db01b48ea900a7d9fce7a7910ff318/constantly-15.1.0-py2.py3-none-any.whl",
    )
