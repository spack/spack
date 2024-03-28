# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStestr(PythonPackage):
    """A parallel Python test runner built around subunit."""

    homepage = "https://stestr.readthedocs.io/en/latest/"
    pypi = "stestr/stestr-2.5.1.tar.gz"

    license("Apache-2.0")

    version(
        "2.5.1",
        sha256="a99f734775363291496b8300f5dccfd092f0c5c6fc2ec6ccdb27d070c44edf13",
        url="https://pypi.org/packages/67/6f/076614ec71c69ba2c2bfc28e69b50db87e786b369b106c7006ac10623604/stestr-2.5.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cliff@2.8:", when="@2.2:")
        depends_on("py-fixtures@3:", when="@2.2:")
        depends_on("py-future", when="@2.2:4.0")
        depends_on("py-pbr@2:2.0,3,4.0.4:", when="@2.2:")
        depends_on("py-python-subunit@1.3:", when="@2.2:2")
        depends_on("py-pyyaml", when="@2.2:")
        depends_on("py-six@1.10:", when="@2.2:2")
        depends_on("py-testtools@2.2:", when="@2.2:")
        depends_on("py-voluptuous@0.8.9:", when="@2.2:")
