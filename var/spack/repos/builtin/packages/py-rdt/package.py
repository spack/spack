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
        "1.10.0",
        sha256="071c5525e2125f56dd2a01dce72c2adaa4f2465cbb86183b8815e540d38c83fb",
        url="https://pypi.org/packages/3b/c0/4c1c771a2f839b564cd6cac4d66e44655548bba22cbe73089257e5f4c2bb/rdt-1.10.0-py3-none-any.whl",
    )
    version(
        "0.6.4",
        sha256="72d8a5567c5a50eded47ef4bd0ebdb13650852576ca5692bc4b04eb0539d8498",
        url="https://pypi.org/packages/6b/5c/f6184a133796ff66f65a73786972ecc19dd94a13634449892ac6dee2790c/rdt-0.6.4-py2.py3-none-any.whl",
    )
    version(
        "0.6.1",
        sha256="e1c9d4c2733deb95ae1fd97848661f963ef57b79f3d1ed9fabc6bc0715029965",
        url="https://pypi.org/packages/0b/0e/1b3a505ada571f07a9c4ead7eb2f2130722056e968e5fb2c8bcb370c9f88/rdt-0.6.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3.11", when="@1.5.1.dev1:")
        depends_on("python@:3.9", when="@0.6.1:1.2,1.3.0.dev:1.3.0.dev0")
        depends_on("py-faker@17:19", when="@1.8:")
        depends_on("py-numpy@1.23.3:1", when="@1.3: ^python@3.10:")
        depends_on("py-numpy@1.20.0:1", when="@1.3: ^python@:3.9")
        depends_on("py-numpy@1.20.0:1", when="@0.6.1:1.2,1.3.0.dev:1.3.0.dev0 ^python@3.7:")
        depends_on("py-numpy@1.18.0:1.19", when="@0.6.1:1.2,1.3.0.dev:1.3.0.dev0 ^python@:3.6")
        depends_on("py-pandas@1.5.0:", when="@1.4.2: ^python@3.11:")
        depends_on("py-pandas@1.3.4:", when="@1.4.2: ^python@3.10")
        depends_on("py-pandas@1.1.3:", when="@1.4.2: ^python@:3.9")
        depends_on("py-pandas@1.1.3:1", when="@0.6.2:1.2,1.3.0.dev:1.3.0.dev0")
        depends_on("py-pandas@1.1.3:1.1.4", when="@0.6.1")
        depends_on("py-psutil@5.7:", when="@:1.7")
        depends_on("py-pyyaml@5.4.1:5", when="@0.6.2:1.2,1.3.0.dev:1.3.0.dev0")
        depends_on("py-scikit-learn@1.1.3:", when="@1.9.3: ^python@3.11:")
        depends_on("py-scikit-learn@1.1.0:", when="@1.9.3: ^python@3.10")
        depends_on("py-scikit-learn@0.24.0:", when="@1.3: ^python@:3.9")
        depends_on("py-scikit-learn@0.24.0:", when="@0.6.3:1.2,1.3.0.dev:1.3.0.dev0")
        depends_on("py-scipy@1.9.2:", when="@1.3: ^python@3.10:")
        depends_on("py-scipy@1.5.4:", when="@1.3: ^python@:3.9")
        depends_on("py-scipy@1.5.4:1.7", when="@0.6.4:1.2,1.3.0.dev:1.3.0.dev0")
        depends_on("py-scipy@1.5.4:", when="@0.6.1:0.6.3")
