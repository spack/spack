# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribJsmath(PythonPackage):
    """A sphinx extension which renders display math in HTML via JavaScript."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-jsmath/sphinxcontrib-jsmath-1.0.1.tar.gz"

    # 'sphinx' requires 'sphinxcontrib-jsmath' at build-time, but
    # 'sphinxcontrib-jsmath' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version(
        "1.0.1",
        sha256="2ec2eaebfb78f3f2078e73666b1415417a116cc848b72e5172e596c871103178",
        url="https://pypi.org/packages/c2/42/4c8646762ee83602e3fb3fbe774c2fac12f317deb0b5dbeeedd2d3ba4b77/sphinxcontrib_jsmath-1.0.1-py2.py3-none-any.whl",
    )
