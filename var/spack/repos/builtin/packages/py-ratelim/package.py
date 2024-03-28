# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRatelim(PythonPackage):
    """Makes it easy to respect rate limits."""

    homepage = "https://github.com/themiurgo/ratelim"
    pypi = "ratelim/ratelim-0.1.6.tar.gz"

    license("MIT")

    version(
        "0.1.6",
        sha256="e1a7dd39e6b552b7cc7f52169cd66cdb826a1a30198e355d7016012987c9ad08",
        url="https://pypi.org/packages/f2/98/7e6d147fd16a10a5f821db6e25f192265d6ecca3d82957a4fdd592cad49c/ratelim-0.1.6-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-decorator", when="@0.1.5:")
