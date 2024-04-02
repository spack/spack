# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlatbuffers(PythonPackage):
    """
    The FlatBuffers serialization format implemented in Python. For a faster and
    feature-complete version check out the C++ implementation in `flatbuffers`
    package.
    """

    homepage = "https://google.github.io/flatbuffers/"
    pypi = "flatbuffers/flatbuffers-2.0.tar.gz"

    maintainers("gperrotta")

    license("Apache-2.0")

    version(
        "23.5.26",
        sha256="c0ff356da363087b915fde4b8b45bdda73432fc17cddb3c8157472eab1422ad1",
        url="https://pypi.org/packages/6f/12/d5c79ee252793ffe845d58a913197bfa02ae9a0b5c9bc3dc4b58d477b9e7/flatbuffers-23.5.26-py2.py3-none-any.whl",
    )
    version(
        "2.0.7",
        sha256="71e135d533be527192819aaab757c5e3d109cb10fbb01e687f6bdb7a61ad39d1",
        url="https://pypi.org/packages/d7/0d/b5bfb553a6ac66d6ec2b6d7f1e814a908fba7188356ac94bb36ae3d905c3/flatbuffers-2.0.7-py2.py3-none-any.whl",
    )
    version(
        "2.0",
        sha256="3751954f0604580d3219ae49a85fafec9d85eec599c0b96226e1bc0b48e57474",
        url="https://pypi.org/packages/3d/d0/26033c70d642fbc1e35d3619cf3210986fb953c173b1226709f75056c149/flatbuffers-2.0-py2.py3-none-any.whl",
    )
    version(
        "1.12",
        sha256="9e9ef47fa92625c4721036e7c4124182668dc6021d9e7c73704edd395648deb9",
        url="https://pypi.org/packages/eb/26/712e578c5f14e26ae3314c39a1bdc4eb2ec2f4ddc89b708cf8e0a0d20423/flatbuffers-1.12-py2.py3-none-any.whl",
    )
