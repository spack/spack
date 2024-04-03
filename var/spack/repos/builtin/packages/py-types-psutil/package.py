# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesPsutil(PythonPackage):
    """Typing stubs for psutil."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-psutil/types-psutil-5.9.5.5.tar.gz"

    version(
        "5.9.5.16",
        sha256="fec713104d5d143afea7b976cfa691ca1840f5d19e8714a5d02a96ebd061363e",
        url="https://pypi.org/packages/36/0a/fd3b20a2ad38da85fde049ec013930d546b2a77300a9d5cf407161fcacf1/types_psutil-5.9.5.16-py3-none-any.whl",
    )
    version(
        "5.9.5.5",
        sha256="e576bb81c74f7443b067e94f92435894d5dd561161bec3d6401727b63df009f0",
        url="https://pypi.org/packages/94/7d/e74be3fb36b7816e57dc8e9f7a21062629715cbe92ba2f12b74db5d188fa/types_psutil-5.9.5.5-py3-none-any.whl",
    )
