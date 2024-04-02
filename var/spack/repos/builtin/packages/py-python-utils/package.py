# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonUtils(PythonPackage):
    """Python Utils is a collection of small Python functions and classes
    which make common patterns shorter and easier."""

    homepage = "https://github.com/WoLpH/python-utils"
    pypi = "python-utils/python-utils-2.4.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.5.2",
        sha256="8bfefc3430f1c48408fa0e5958eee51d39840a5a987c2181a579e99ab6fe5ca6",
        url="https://pypi.org/packages/79/80/4276fba30da6ed26165b67093ce4a2ca78b701a55920d39e59cc82ee9639/python_utils-3.5.2-py2.py3-none-any.whl",
    )
    version(
        "2.7.1",
        sha256="9d535eda3fd4c0cd51f459bb9cfddd983a50f5adfacb0995504d12bf0c2981cb",
        url="https://pypi.org/packages/0a/c2/962e0ec22173309d8914733dc78cf8a689fe2ae612938ec64c26d0f29ac6/python_utils-2.7.1-py2.py3-none-any.whl",
    )
    version(
        "2.4.0",
        sha256="ebaadab29d0cb9dca0a82eab9c405f5be5125dbbff35b8f32cc433fa498dbaa7",
        url="https://pypi.org/packages/d9/ff/623dfa533f3277199957229f053fdb2c73a9c18048680e1899c9a5c95e6b/python_utils-2.4.0-py2.py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="e25f840564554eaded56eaa395bca507b0b9e9f0ae5ecb13a8cb785305c56d25",
        url="https://pypi.org/packages/eb/a0/19119d8b7c05be49baf6c593f11c432d571b70d805f2fe94c0585e55e4c8/python_utils-2.3.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@2.6:2")
        depends_on("py-typing-extensions", when="@3.5 ^python@:3.7")
