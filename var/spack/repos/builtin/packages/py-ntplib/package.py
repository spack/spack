# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNtplib(PythonPackage):
    """Simple interface to query NTP servers from Python."""

    homepage = "https://github.com/cf-natali/ntplib"
    git = "https://github.com/cf-natali/ntplib.git"
    pypi = "ntplib/ntplib-0.4.0.tar.gz"

    license("MIT")

    version(
        "0.4.0",
        sha256="8d27375329ed7ff38755f7b6d4658b28edc147cadf40338a63a0da8133469d60",
        url="https://pypi.org/packages/58/8c/41da70f6feaca807357206a376b6de2001b439c7f78f53473a914a6dbd1e/ntplib-0.4.0-py2.py3-none-any.whl",
    )
