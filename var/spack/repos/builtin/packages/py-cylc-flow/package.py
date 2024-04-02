# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylcFlow(PythonPackage):
    """A workflow engine for cycling systems."""

    homepage = "https://cylc.org"
    pypi = "cylc-flow/cylc-flow-8.1.4.tar.gz"

    maintainers("LydDeb", "climbfuji")

    license("GPL-3.0-only")

    version(
        "8.2.3",
        sha256="ad09fd8072f7bc47b0adf3c29deeb9e52d81e151f651beb689f10b7d083d5af6",
        url="https://pypi.org/packages/cf/1f/8b9f6faff518138d7220cefd1aa01721ad1326b21ed2c94b8c3bbc6ff8cc/cylc_flow-8.2.3-py3-none-any.whl",
    )
    version(
        "8.2.0",
        sha256="62bb7201f6aae8258749bd0065bd71c538116f72bb1e711028b9f4812fd59e01",
        url="https://pypi.org/packages/7f/39/8958c62393ce821730058b0bf4686480302a9982f5716fa94c0539a30403/cylc_flow-8.2.0-py3-none-any.whl",
    )
    version(
        "8.1.4",
        sha256="da404e7f6b3e5204fe1fb613602bb1e3be6aea6895999630a62d21833be3c359",
        url="https://pypi.org/packages/de/2c/bdaba24b3fa802153f23bfea21149502e5a57210fcb20033d16e0b8d1900/cylc_flow-8.1.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-aiofiles@0.7", when="@:8.1")
        depends_on("py-ansimarkup@1:")
        depends_on("py-async-timeout@3:")
        depends_on("py-colorama@0.4:")
        depends_on("py-graphene@2.1:2")
        depends_on("py-importlib-metadata", when="@8.1.3: ^python@:3.7")
        depends_on("py-jinja2@3:3.0", when="@8.0.0:")
        depends_on("py-metomi-isodatetime@1.3:", when="@8.2.3:")
        depends_on("py-metomi-isodatetime@1.3:1.3.0", when="@8.0-rc3:8.2.2")
        depends_on("py-promise", when="@8.0-rc3:")
        depends_on("py-protobuf@4.21.2:4.21", when="@8.1:")
        depends_on("py-psutil@5.6:")
        depends_on("py-pyzmq@22:", when="@8.2:")
        depends_on("py-pyzmq@22", when="@:8.1")
        depends_on("py-rx", when="@8.0-rc3:")
        depends_on("py-setuptools@49:66,68:", when="@8.2:")
        depends_on("py-setuptools@49:66", when="@8.1")
        depends_on("py-tomli@2:", when="@8.1: ^python@:3.10")
        depends_on("py-urwid@2:")

    # Non-Python dependencies
