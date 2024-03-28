# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAioitertools(PythonPackage):
    """Implementation of itertools, builtins, and more for AsyncIO and mixed-type
    iterables."""

    homepage = "https://aioitertools.omnilib.dev/en/stable/"
    pypi = "aioitertools/aioitertools-0.7.1.tar.gz"

    license("MIT")

    version(
        "0.11.0",
        sha256="04b95e3dab25b449def24d7df809411c10e62aab0cbe31a50ca4e68748c43394",
        url="https://pypi.org/packages/45/66/d1a9fd8e6ff88f2157cb145dd054defb0fd7fe2507fe5a01347e7c690eab/aioitertools-0.11.0-py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="8972308474c41ed5e0636819f948ebff32f2318e70f7e7d23cd208c4357cc773",
        url="https://pypi.org/packages/32/0b/3260ac050de07bf6e91871944583bb8598091da19155c34f7ef02244709c/aioitertools-0.7.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-typing-extensions@4:", when="@0.9: ^python@:3.9")
        depends_on("py-typing-extensions@3.7:", when="@0.7")
