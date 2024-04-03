# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackoff(PythonPackage):
    """Function decoration for backoff and retry."""

    homepage = "https://github.com/litl/backoff"
    pypi = "backoff/backoff-2.2.1.tar.gz"

    license("MIT")

    version(
        "2.2.1",
        sha256="63579f9a0628e06278f7e47b7d7d5b6ce20dc65c5e96a6f3ca99a6adca0396e8",
        url="https://pypi.org/packages/df/73/b6e24bd22e6720ca8ee9a85a0c4a2971af8497d8f3193fa05390cbd46e09/backoff-2.2.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@2:")
