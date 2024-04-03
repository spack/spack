# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetomiRose(PythonPackage):
    """Rose, a framework for meteorological suites."""

    homepage = "https://metomi.github.io/rose/doc/html/index.html"
    pypi = "metomi-rose/metomi-rose-2.1.0.tar.gz"

    maintainers("LydDeb")

    license("GPL-3.0-only")

    version(
        "2.1.0",
        sha256="ffabd2f48e328debbc6421f4eba80a36b61c70b41a2bd6388b7892eef5cd6cb0",
        url="https://pypi.org/packages/a0/39/c688c5a81624032df8f0a36b083e06be85b80a1abf8587967af902c91c74/metomi_rose-2.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.0-rc1:")
        depends_on("py-aiofiles")
        depends_on("py-jinja2@2.10.1:")
        depends_on("py-keyring@23", when="@2.1:")
        depends_on("py-ldap3")
        depends_on("py-metomi-isodatetime@1.3:", when="@2.0-rc3:")
        depends_on("py-psutil@5.6:")
        depends_on("py-requests")
        depends_on("py-sqlalchemy@1", when="@2.0.3:")
