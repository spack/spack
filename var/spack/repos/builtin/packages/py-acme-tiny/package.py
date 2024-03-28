# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAcmeTiny(PythonPackage):
    """A tiny script to issue and renew TLS certs from Let's Encrypt."""

    homepage = "https://github.com/diafygi/acme-tiny"
    git = "https://github.com/diafygi/acme-tiny.git"

    license("MIT")

    version(
        "4.0.4",
        sha256="70ab30bbbbcfadbf68ca47b4d991fe12cd5126574a6fb0ead7985f8885ee30b0",
        url="https://pypi.org/packages/96/4f/19c6a31d6f520fdca0e2e03003c94d34b21a131ebe3b82da1953075e7bea/acme_tiny-4.0.4-py2.py3-none-any.whl",
    )
