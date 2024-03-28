# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUrllib3SecureExtra(PythonPackage):
    """Marker library to detect whether urllib3 was installed with the deprecated [secure] extra"""

    homepage = "https://github.com/urllib3/urllib3-secure-extra"
    pypi = "urllib3-secure-extra/urllib3-secure-extra-0.1.0.tar.gz"

    version(
        "0.1.0",
        sha256="f7adcb108b4d12a4b26b99eb60e265d087f435052a76aefa396b6ee85e9a6ef9",
        url="https://pypi.org/packages/90/cd/273b6978ace72ef1d3f35610206e44e4527d557500e3d7b39732f2b4dd3c/urllib3_secure_extra-0.1.0-py2.py3-none-any.whl",
    )
