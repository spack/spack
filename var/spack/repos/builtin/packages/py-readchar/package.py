# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReadchar(PythonPackage):
    """Library to easily read single chars and key strokes."""

    homepage = "https://github.com/magmax/python-readchar"
    pypi = "readchar/readchar-4.0.5.tar.gz"

    license("MIT")

    version(
        "4.0.5",
        sha256="76ec784a5dd2afac3b7da8003329834cdd9824294c260027f8c8d2e4d0a78f43",
        url="https://pypi.org/packages/cd/14/730280df294e52e395a70111f4d9b07be94f5ba7a69db7eba3c324f113b2/readchar-4.0.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@4.0.4:4.0.5")
        depends_on("py-setuptools@41:", when="@4.0.3:")
