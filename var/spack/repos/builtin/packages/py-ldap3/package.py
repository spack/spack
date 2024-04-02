# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLdap3(PythonPackage):
    """A strictly RFC 4510 conforming LDAP V3 pure Python client library."""

    homepage = "https://github.com/cannatag/ldap3"
    pypi = "ldap3/ldap3-2.9.1.tar.gz"

    maintainers("LydDeb")

    license("LGPL-3.0-or-later")

    version(
        "2.9.1",
        sha256="5869596fc4948797020d3f03b7939da938778a0f9e2009f7a072ccf92b8e8d70",
        url="https://pypi.org/packages/4e/f6/71d6ec9f18da0b2201287ce9db6afb1a1f637dedb3f0703409558981c723/ldap3-2.9.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pyasn1@0.4.6:", when="@2.8:")
