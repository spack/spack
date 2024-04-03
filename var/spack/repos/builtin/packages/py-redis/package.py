# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRedis(PythonPackage):
    """The Python interface to the Redis key-value store."""

    homepage = "https://github.com/redis/redis-py"
    pypi = "redis/redis-3.3.8.tar.gz"

    license("MIT")

    version(
        "4.5.1",
        sha256="5deb072d26e67d2be1712603bfb7947ec3431fb0eec9c578994052e33035af6d",
        url="https://pypi.org/packages/06/b5/328851ee54bbf00cc609671a658e0420d88aa2b4f5ace7aa669932d59a0e/redis-4.5.1-py3-none-any.whl",
    )
    version(
        "3.5.3",
        sha256="432b788c4530cfe16d8d943a09d40ca6c16149727e4afe8c2c9d5580c59d9f24",
        url="https://pypi.org/packages/a7/7c/24fb0511df653cf1a5d938d8f5d19802a88cef255706fdda242ff97e91b7/redis-3.5.3-py2.py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="174101a3ce04560d716616290bb40e0a2af45d5844c8bd474c23fc5c52e7a46a",
        url="https://pypi.org/packages/d2/07/20cb8df2ded4b5db176a65da48b7c8d4295d868776296580b11071218a2b/redis-3.5.0-py2.py3-none-any.whl",
    )
    version(
        "3.3.8",
        sha256="c504251769031b0dd7dd5cf786050a6050197c6de0d37778c80c08cb04ae8275",
        url="https://pypi.org/packages/bd/64/b1e90af9bf0c7f6ef55e46b81ab527b33b785824d65300bb65636534b530/redis-3.3.8-py2.py3-none-any.whl",
    )

    variant(
        "hiredis",
        default=False,
        description="Support for hiredis which speeds up parsing of multi bulk replies",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@4.4:5.1.0-alpha1")
        depends_on("py-async-timeout@4.0.2:", when="@4.2:4.5.1")
        depends_on("py-hiredis@1:", when="@4.0.0-rc1:+hiredis")
        depends_on("py-hiredis@0.1.3:", when="@:3+hiredis")
        depends_on("py-importlib-metadata@1:", when="@4.1.0:5.1.0-alpha1 ^python@:3.7")
        depends_on("py-typing-extensions", when="@4.2.1:5.1.0-alpha1,5.1.0-beta3 ^python@:3.7")
