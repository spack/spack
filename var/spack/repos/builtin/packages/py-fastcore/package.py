# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastcore(PythonPackage):
    """Python is a powerful, dynamic language. Rather than bake
    everything into the language, it lets the programmer
    customize it to make it work for them. fastcore uses this
    flexibility to add to Python features inspired by other
    languages we've loved, like multiple dispatch from Julia,
    mixins from Ruby, and currying, binding, and more from
    Haskell. It also adds some "missing features" and clean up
    some rough edges in the Python standard library, such as
    simplifying parallel processing, and bringing ideas from
    NumPy over to Python's list type."""

    homepage = "https://github.com/fastai/fastcore/tree/master/"
    pypi = "fastcore/fastcore-1.3.27.tar.gz"

    license("Apache-2.0")

    version(
        "1.3.27",
        sha256="03c6c93f2c769fdd611e32a7cc1433db5a82f67146d9e2f88e03107db203f6de",
        url="https://pypi.org/packages/50/2b/832378cc02c608798fe13baec2709e70e3796459e6936c4bd3ee7edc4345/fastcore-1.3.27-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-packaging")
        depends_on("py-pip")
