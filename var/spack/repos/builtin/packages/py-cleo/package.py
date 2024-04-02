# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCleo(PythonPackage):
    """Cleo allows you to create beautiful and testable command-line interfaces."""

    homepage = "https://github.com/sdispater/cleo"
    pypi = "cleo/cleo-0.8.1.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version(
        "2.1.0",
        sha256="4a31bd4dd45695a64ee3c4758f583f134267c2bc518d8ae9a29cf237d009b07e",
        url="https://pypi.org/packages/2d/f5/6bbead8b880620e5a99e0e4bb9e22e67cca16ff48d54105302a3e7821096/cleo-2.1.0-py3-none-any.whl",
    )
    version(
        "2.0.1",
        sha256="6eb133670a3ed1f3b052d53789017b6e50fca66d1287e6e6696285f4cb8ea448",
        url="https://pypi.org/packages/b1/ae/0329af2a4c22836010c43760233a181a314853a97e0f2b53b02825c4c9b7/cleo-2.0.1-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="daad7ff76134ebe2c7bf74520b1bbd59e6e77026535b967efc5a15a0eaa2e19c",
        url="https://pypi.org/packages/54/0f/8d81e21eca2da9be67801f8f3faf37a057cf88dac31c0ef3644beb11244e/cleo-2.0.0-py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="38b8889a94b769aa021f7e759afb08546647a3fc701222d2d584039c246c6aed",
        url="https://pypi.org/packages/b8/07/e2bcedbc314014e4422e49bcd7befcdb53cd81275a002d02e6aa01707f7f/cleo-1.0.0-py3-none-any.whl",
    )
    version(
        "1.0.0-alpha5",
        sha256="ff53056589300976e960f75afb792dfbfc9c78dcbb5a448e207a17b643826360",
        url="https://pypi.org/packages/45/0c/3825603bf62f360829b1eea29a43dadce30829067e288170b3bf738aafd0/cleo-1.0.0a5-py3-none-any.whl",
    )
    version(
        "0.8.1",
        sha256="141cda6dc94a92343be626bb87a0b6c86ae291dfc732a57bf04310d4b4201753",
        url="https://pypi.org/packages/09/46/3577da4237675e90630e8e9ccd2c7dbcd42afd4463712a207eab148dfbc2/cleo-0.8.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@1.0.0-alpha5:")
        depends_on("py-clikit@0.6:", when="@0.8.1:0")
        depends_on("py-crashtest@0.4.1:", when="@1.0.0:")
        depends_on("py-crashtest@0.3.1:0.3", when="@1:1.0.0-alpha5")
        depends_on("py-pylev@1.3:", when="@:0.7.4,1:1.0.0-alpha5")
        depends_on("py-rapidfuzz@3:", when="@2.1:")
        depends_on("py-rapidfuzz@2.2:2", when="@1.0.0:2.0")
