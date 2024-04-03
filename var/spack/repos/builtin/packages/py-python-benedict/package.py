# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonBenedict(PythonPackage):
    """A dict subclass with keylist/keypath support, I/O shortcuts
    and many utilities."""

    homepage = "https://github.com/fabiocaccamo/python-benedict"
    pypi = "python-benedict/python-benedict-0.22.2.tar.gz"

    license("MIT")

    version(
        "0.23.2",
        sha256="b484901d94eb5b8aabd3e612cf1c504b42a92b6f17506428c60dbf93c3a88c6e",
        url="https://pypi.org/packages/87/c8/ae31902c3e6f671580e14472ca23d4b19831085999ff34ee00a22f648e84/python_benedict-0.23.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-ftfy", when="@:0.24")
        depends_on("py-mailchecker", when="@:0.24")
        depends_on("py-phonenumbers", when="@:0.24")
        depends_on("py-python-dateutil", when="@:0.24")
        depends_on("py-python-fsutil", when="@0.23:0.24")
        depends_on("py-python-slugify", when="@:0.24")
        depends_on("py-pyyaml", when="@:0.24")
        depends_on("py-requests", when="@:0.24")
        depends_on("py-six", when="@:0.24")
        depends_on("py-toml", when="@:0.24")
        depends_on("py-xmltodict", when="@:0.24")
