# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebencodings(PythonPackage):
    """This is a Python implementation of the WHATWG Encoding standard."""

    homepage = "https://github.com/gsnedders/python-webencodings"
    pypi = "webencodings/webencodings-0.5.1.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.5.1",
        sha256="a0af1213f3c2226497a97e2b3aa01a7e4bee4f403f95be16fc9acd2947514a78",
        url="https://pypi.org/packages/f4/24/2a3e3df732393fed8b3ebf2ec078f05546de641fe1b667ee316ec1dcf3b7/webencodings-0.5.1-py2.py3-none-any.whl",
    )
