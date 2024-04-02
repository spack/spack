# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCmakeFormat(PythonPackage):
    """cmake-format project provides Quality Assurance (QA) tools for
    cmake. Tools include cmake-annotate, cmake-format, cmake-lint,
    and ctest-to."""

    pypi = "cmake_format/cmake_format-0.6.9.tar.gz"

    version(
        "0.6.11",
        sha256="831d97ea92208e58c3ee2480939dfb07a52ab05e1e103f4a42139e7bbf7c8cb1",
        url="https://pypi.org/packages/42/35/df6eba13d8b20b01bad78a492cd13ed4179c28a2a058cd84884a979507e7/cmake_format-0.6.11-py3-none-any.whl",
    )
    version(
        "0.6.10",
        sha256="8a7dab8381d961a56ea111aeb0d0d6887df385ee2aa6b026a03fdd89bd683e94",
        url="https://pypi.org/packages/63/00/cc2609916eb0ddb636619350e2bdf8b96e509ca65a44860bd11f6287e143/cmake_format-0.6.10-py3-none-any.whl",
    )
    version(
        "0.6.9",
        sha256="240d44d8c4a62153e53b34add4f072d38b495beae892a95c0b1cc7c5a172a21b",
        url="https://pypi.org/packages/76/5a/ed2b1a1bc3622e85c56de96f64d38b27888ce6082e47b5106e176a064a91/cmake_format-0.6.9-py3-none-any.whl",
    )

    variant("htmlgen", default=False, description="Support for HTML annotator")
    variant("yaml", default=False, description="Support for YAML config files")

    with default_args(type="run"):
        depends_on("py-pyyaml@5.3:", when="@0.6.8:+yaml")
        depends_on("py-six@1.13:", when="@0.6.8:0.6.11")
