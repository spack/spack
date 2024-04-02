# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScooby(PythonPackage):
    """A Great Dane turned Python environment detective."""

    homepage = "https://github.com/banesullivan/scooby"
    pypi = "scooby/scooby-0.5.7.tar.gz"

    license("MIT")

    version(
        "0.5.7",
        sha256="bc5ebc6919965e8591623ad2c24fe91f40941e5e73038999ccf5de4a31439f68",
        url="https://pypi.org/packages/1b/99/db6d34bdc3f060d631f524c2f0fc4b1919cd3bf734c905fc1b25eb847ac2/scooby-0.5.7-py3-none-any.whl",
    )
