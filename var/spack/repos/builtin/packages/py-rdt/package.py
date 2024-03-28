# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRdt(PythonPackage):
    """RDT is a Python library used to transform data for data
    science libraries and preserve the transformations in order
    to revert them as needed."""

    homepage = "https://github.com/sdv-dev/RDT"
    pypi = "rdt/rdt-0.6.1.tar.gz"

    license("MIT")

    version(
        "0.6.1",
        sha256="e1c9d4c2733deb95ae1fd97848661f963ef57b79f3d1ed9fabc6bc0715029965",
        url="https://pypi.org/packages/0b/0e/1b3a505ada571f07a9c4ead7eb2f2130722056e968e5fb2c8bcb370c9f88/rdt-0.6.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.11", when="@1.3:")
        depends_on("python@:3.9", when="@0.6.1:1.2,1.3.0.dev:1.3.0.dev0")
        depends_on("python@:3.8", when="@0.2.4:0.6.0")
        depends_on("py-numpy@1.20.0:1", when="@1.3: ^python@:3.9")
        depends_on("py-numpy@1.20.0:1", when="@0.6.1:1.2,1.3.0.dev:1.3.0.dev0")
        depends_on("py-pandas@1.1.3:1.1.4", when="@0.6.1")
        depends_on("py-psutil@5.7:", when="@0.5.1:1.7")
        depends_on("py-scikit-learn@0.24.0:0", when="@0.6.2,0.6.3.dev:0.6.3.dev2")
        depends_on("py-scipy@1.5.4:", when="@1.3: ^python@:3.9")
        depends_on("py-scipy@1.5.4:", when="@0.6.1:0.6.3")
