# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUritemplate(PythonPackage):
    """Simple python library to deal with URI Templates."""

    homepage = "https://uritemplate.readthedocs.org/"
    pypi = "uritemplate/uritemplate-3.0.0.tar.gz"

    license("Apache-2.0")

    version(
        "4.1.1",
        sha256="830c08b8d99bdd312ea4ead05994a38e8936266f84b9a7878232db50b044e02e",
        url="https://pypi.org/packages/81/c0/7461b49cd25aeece13766f02ee576d1db528f1c37ce69aee300e075b485b/uritemplate-4.1.1-py2.py3-none-any.whl",
    )
    version(
        "3.0.0",
        sha256="1b9c467a940ce9fb9f50df819e8ddd14696f89b9a8cc87ac77952ba416e0a8fd",
        url="https://pypi.org/packages/e5/7d/9d5a640c4f8bf2c8b1afc015e9a9d8de32e13c9016dcc4b0ec03481fb396/uritemplate-3.0.0-py2.py3-none-any.whl",
    )
