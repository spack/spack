# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAspyYaml(PythonPackage):
    """Some extensions to pyyaml."""

    homepage = "https://github.com/asottile/aspy.yaml/"
    pypi = "aspy.yaml/aspy.yaml-1.3.0.tar.gz"

    license("MIT")

    version(
        "1.3.0",
        sha256="463372c043f70160a9ec950c3f1e4c3a82db5fca01d334b6bc89c7164d744bdc",
        url="https://pypi.org/packages/99/ce/78be097b00817ccf02deaf481eb7a603eecee6fa216e82fa7848cd265449/aspy.yaml-1.3.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pyyaml", when="@0.2.2:")
