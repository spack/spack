# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEmailValidator(PythonPackage):
    """A robust email address syntax and deliverability validation library."""

    homepage = "https://github.com/JoshData/python-email-validator"
    pypi = "email_validator/email_validator-1.3.1.tar.gz"

    version("1.3.1", sha256="d178c5c6fa6c6824e9b04f199cf23e79ac15756786573c190d2ad13089411ad2")

    depends_on("py-setuptools", type="build")
    depends_on("py-dnspython@1.15:", type=("build", "run"))
    depends_on("py-idna@2:", type=("build", "run"))
