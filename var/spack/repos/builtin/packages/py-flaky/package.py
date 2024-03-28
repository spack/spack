# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaky(PythonPackage):
    """Flaky is a plugin for nose or pytest that automatically reruns flaky tests."""

    homepage = "https://github.com/box/flaky"
    pypi = "flaky/flaky-3.7.0.tar.gz"

    version(
        "3.7.0",
        sha256="d6eda73cab5ae7364504b7c44670f70abed9e75f77dd116352f662817592ec9c",
        url="https://pypi.org/packages/43/0e/2f50064e327f41a1eb811df089f813036e19a64b95e33f8e9e0b96c2447e/flaky-3.7.0-py2.py3-none-any.whl",
    )
