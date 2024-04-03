# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRfc3339Validator(PythonPackage):
    """A pure python RFC3339 validator."""

    homepage = "https://github.com/naimetti/rfc3339-validator"
    pypi = "rfc3339_validator/rfc3339_validator-0.1.4.tar.gz"

    license("MIT")

    version(
        "0.1.4",
        sha256="24f6ec1eda14ef823da9e36ec7113124b39c04d50a4d3d3a3c2859577e7791fa",
        url="https://pypi.org/packages/7b/44/4e421b96b67b2daff264473f7465db72fbdf36a07e05494f50300cc7b0c6/rfc3339_validator-0.1.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six")
