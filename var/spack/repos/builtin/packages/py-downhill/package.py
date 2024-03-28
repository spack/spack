# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDownhill(PythonPackage):
    """Stochastic optimization routines for Theano"""

    homepage = "http://github.com/lmjohns3/downhill"
    pypi = "downhill/downhill-0.4.0.tar.gz"

    license("MIT")

    version(
        "0.4.0",
        sha256="29e3dbf4db13021734c5bbef0eef230a17c49dfd4155a41016b712f909868f1b",
        url="https://pypi.org/packages/32/07/fb2b465371d80d5686328640f31ad403193fe91d527cca538ff1834880b1/downhill-0.4.0-py2.py3-none-any.whl",
    )
