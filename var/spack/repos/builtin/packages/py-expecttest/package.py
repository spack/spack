# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExpecttest(PythonPackage):
    """This library implements expect tests (also known as "golden" tests)."""

    homepage = "https://github.com/ezyang/expecttest"
    pypi = "expecttest/expecttest-0.1.6.tar.gz"

    license("MIT")

    version(
        "0.1.6",
        sha256="7cf2db203c06f9e3173670ca9d09ac00912e535139afac2c7458c1627b1a3ee6",
        url="https://pypi.org/packages/c7/39/689391845f5dc48df81b0c22248d5f66919b82da12f2bab1424bc3610529/expecttest-0.1.6-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@:0.1")
