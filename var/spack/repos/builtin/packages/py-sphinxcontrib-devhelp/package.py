# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribDevhelp(PythonPackage):
    """sphinxcontrib-devhelp is a sphinx extension which outputs
    Devhelp document."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-devhelp/sphinxcontrib-devhelp-1.0.1.tar.gz"
    git = "https://github.com/sphinx-doc/sphinxcontrib-devhelp.git"

    # 'sphinx' requires 'sphinxcontrib-devhelp' at build-time, but
    # 'sphinxcontrib-devhelp' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version(
        "1.0.2",
        sha256="8165223f9a335cc1af7ffe1ed31d2871f325254c0423bc0c4c7cd1c1e4734a2e",
        url="https://pypi.org/packages/c5/09/5de5ed43a521387f18bdf5f5af31d099605c992fd25372b2b9b825ce48ee/sphinxcontrib_devhelp-1.0.2-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="9512ecb00a2b0821a146736b39f7aeb90759834b07e81e8cc23a9c70bacb9981",
        url="https://pypi.org/packages/b0/a3/fea98741f0b2f2902fbf6c35c8e91b22cd0dd13387291e81d457f9a93066/sphinxcontrib_devhelp-1.0.1-py2.py3-none-any.whl",
    )
