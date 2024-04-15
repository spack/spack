# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCrashtest(PythonPackage):
    """Crashtest is a Python library that makes exceptions handling
    and inspection easier."""

    homepage = "https://github.com/sdispater/crashtest"
    pypi = "crashtest/crashtest-0.3.1.tar.gz"

    license("MIT")

    version(
        "0.4.1",
        sha256="8d23eac5fa660409f57472e3851dab7ac18aba459a8d19cbbba86d3d5aecd2a5",
        url="https://pypi.org/packages/b0/5c/3ba7d12e7a79566f97b8f954400926d7b6eb33bcdccc1315a857f200f1f1/crashtest-0.4.1-py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="476839dfa58bb238aa7db8752db7029bfc8bdc87b571d3a15727da8af61b7487",
        url="https://pypi.org/packages/54/c2/7b8c3babedc92d62b3f5f8d2eaa4b969aaa70dba29f05bc7ef7dc3c18494/crashtest-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="300f4b0825f57688b47b6d70c6a31de33512eb2fa1ac614f780939aa0cf91680",
        url="https://pypi.org/packages/76/97/2a99f020be5e4a5a97ba10bc480e2e6a889b5087103a2c6b952b5f819d27/crashtest-0.3.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:3", when="@0.4:")
        depends_on("python@:3", when="@:0.3")
