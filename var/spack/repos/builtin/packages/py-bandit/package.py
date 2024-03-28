# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBandit(PythonPackage):
    """Security oriented static analyser for python code."""

    homepage = "https://bandit.readthedocs.io/en/latest/"
    pypi = "bandit/bandit-1.7.0.tar.gz"

    version(
        "1.7.0",
        sha256="216be4d044209fa06cf2a3e51b319769a51be8318140659719aa7a115c35ed07",
        url="https://pypi.org/packages/6e/68/dc39991eb6074cabeed2ee78f6e101054869f79ba806f8b6e4b1f4f7c3f6/bandit-1.7.0-py3-none-any.whl",
    )
