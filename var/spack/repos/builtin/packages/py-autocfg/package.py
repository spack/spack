# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAutocfg(PythonPackage):
    """Deep learning configuration."""

    homepage = "https://github.com/zhreshold/autocfg"
    pypi = "autocfg/autocfg-0.0.8.tar.gz"

    version(
        "0.0.8",
        sha256="7458f8dc2aff67161a31a7d196c3d34002a34907bace58373394cc3a7107ce2a",
        url="https://pypi.org/packages/95/f9/74e0a42cbc6d871c92288806e7812c7d2628c2a06557930dbab0a17438d2/autocfg-0.0.8-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dataclasses", when="^python@:3.6")
        depends_on("py-pyyaml")
