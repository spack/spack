# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVerspec(PythonPackage):
    """verspec is a Python library for handling software versions and
    specifiers, adapted from the packaging package."""

    homepage = "https://github.com/jimporter/verspec"
    pypi = "verspec/verspec-0.1.0.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.1.0",
        sha256="741877d5633cc9464c45a469ae2a31e801e6dbbaa85b9675d481cda100f11c31",
        url="https://pypi.org/packages/a4/ce/3b6fee91c85626eaf769d617f1be9d2e15c1cca027bbdeb2e0d751469355/verspec-0.1.0-py3-none-any.whl",
    )
