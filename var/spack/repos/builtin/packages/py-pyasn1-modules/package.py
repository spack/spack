# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyasn1Modules(PythonPackage):
    """A collection of ASN.1 modules expressed in form of pyasn1 classes.
    Includes protocols PDUs definition (SNMP, LDAP etc.) and various data
    structures (X.509, PKCS etc.)."""

    homepage = "https://github.com/etingof/pyasn1-modules"
    pypi = "pyasn1-modules/pyasn1-modules-0.2.6.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.2.8",
        sha256="a50b808ffeb97cb3601dd25981f6b016cbb3d31fbf57a8b8a87428e6158d0c74",
        url="https://pypi.org/packages/95/de/214830a981892a3e286c3794f41ae67a4495df1108c3da8a9f62159b9a9d/pyasn1_modules-0.2.8-py2.py3-none-any.whl",
    )
    version(
        "0.2.6",
        sha256="e30199a9d221f1b26c885ff3d87fd08694dbbe18ed0e8e405a2a7126d30ce4c0",
        url="https://pypi.org/packages/be/70/e5ea8afd6d08a4b99ebfc77bd1845248d56cfcf43d11f9dc324b9580a35c/pyasn1_modules-0.2.6-py2.py3-none-any.whl",
    )
    version(
        "0.2.5",
        sha256="f309b6c94724aeaf7ca583feb1cc70430e10d7551de5e36edfc1ae6909bcfb3c",
        url="https://pypi.org/packages/91/f0/b03e00ce9fddf4827c42df1c3ce10c74eadebfb706231e8d6d1c356a4062/pyasn1_modules-0.2.5-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pyasn1@0.4.6:0.4", when="@0.2.6:0.2")
        depends_on("py-pyasn1@0.4", when="@0.2:0.2.5")
