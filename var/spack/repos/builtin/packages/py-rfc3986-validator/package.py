# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRfc3986Validator(PythonPackage):
    """Pure python rfc3986 validator."""

    homepage = "https://github.com/naimetti/rfc3986-validator"
    pypi = "rfc3986_validator/rfc3986_validator-0.1.1.tar.gz"

    license("MIT")

    version(
        "0.1.1",
        sha256="2f235c432ef459970b4306369336b9d5dbdda31b510ca1e327636e01f528bfa9",
        url="https://pypi.org/packages/9e/51/17023c0f8f1869d8806b979a2bffa3f861f26a3f1a66b094288323fba52f/rfc3986_validator-0.1.1-py2.py3-none-any.whl",
    )
