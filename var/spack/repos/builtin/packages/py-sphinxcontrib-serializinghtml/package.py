# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribSerializinghtml(PythonPackage):
    """sphinxcontrib-serializinghtml is a sphinx extension which outputs
    "serialized" HTML files (json and pickle)."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-serializinghtml/sphinxcontrib_serializinghtml-1.1.3.tar.gz"

    # 'sphinx' requires 'sphinxcontrib-serializinghtml' at build-time, but
    # 'sphinxcontrib-serializinghtml' requires 'sphinx' at run-time. Don't bother trying
    # to import any modules.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version(
        "1.1.9",
        sha256="9b36e503703ff04f20e9675771df105e58aa029cfcbc23b8ed716019b7416ae1",
        url="https://pypi.org/packages/95/d6/2e0bda62b2a808070ac922d21a950aa2cb5e4fcfb87e5ff5f86bc43a2201/sphinxcontrib_serializinghtml-1.1.9-py3-none-any.whl",
    )
    version(
        "1.1.5",
        sha256="352a9a00ae864471d3a7ead8d7d79f5fc0b57e8b3f95e9867eb9eb28999b92fd",
        url="https://pypi.org/packages/c6/77/5464ec50dd0f1c1037e3c93249b040c8fc8078fdda97530eeb02424b6eea/sphinxcontrib_serializinghtml-1.1.5-py2.py3-none-any.whl",
    )
    version(
        "1.1.3",
        sha256="db6615af393650bf1151a6cd39120c29abaf93cc60db8c48eb2dddbfdc3a9768",
        url="https://pypi.org/packages/57/b3/3648e48fa5682e61e9839d62de4e23af1795ceb738d68d73bd974257a95c/sphinxcontrib_serializinghtml-1.1.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@1.1.6:")
        depends_on("py-sphinx@5.0.0:", when="@1.1.6:1.1.9")

    # Circular dependency
    # depends_on("py-sphinx@5:", when="@1.1.6:", type=("build", "run"))

    # Historical dependencies
