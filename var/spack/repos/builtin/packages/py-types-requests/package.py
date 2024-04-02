# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesRequests(PythonPackage):
    """Typing stubs for requests."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-requests/types-requests-2.28.10.tar.gz"

    version(
        "2.31.0.2",
        sha256="56d181c85b5925cbc59f4489a57e72a8b2166f18273fd8ba7b6fe0c0b986f12a",
        url="https://pypi.org/packages/06/9b/04bb62f11a6824df5d4568439cf0715118c265d0ffbebeb7cf4b8c9caa15/types_requests-2.31.0.2-py3-none-any.whl",
    )
    version(
        "2.28.10",
        sha256="45b485725ed58752f2b23461252f1c1ad9205b884a1e35f786bb295525a3e16a",
        url="https://pypi.org/packages/07/41/5c0bf629bb4abdda40a5c6966deb36a7435c634e710381c8ad7398e13839/types_requests-2.28.10-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-types-urllib3", when="@:2.31.0.6")
