# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribQthelp(PythonPackage):
    """sphinxcontrib-qthelp is a sphinx extension which outputs QtHelp
    document."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-qthelp/sphinxcontrib-qthelp-1.0.2.tar.gz"
    git = "https://github.com/sphinx-doc/sphinxcontrib-qthelp.git"

    # 'sphinx' requires 'sphinxcontrib-qthelp' at build-time, but
    # 'sphinxcontrib-qthelp' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version(
        "1.0.3",
        sha256="bd9fc24bcb748a8d51fd4ecaade681350aa63009a347a8c14e637895444dfab6",
        url="https://pypi.org/packages/2b/14/05f9206cf4e9cfca1afb5fd224c7cd434dcc3a433d6d9e4e0264d29c6cdb/sphinxcontrib_qthelp-1.0.3-py2.py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="513049b93031beb1f57d4daea74068a4feb77aa5630f856fcff2e50de14e9a20",
        url="https://pypi.org/packages/ce/5b/4747c3ba98b3a3e21a66faa183d8f79b9ded70e74212a7988d236a6eb78a/sphinxcontrib_qthelp-1.0.2-py2.py3-none-any.whl",
    )
