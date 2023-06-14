# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribApplehelp(PythonPackage):
    """sphinxcontrib-applehelp is a sphinx extension which outputs Apple
    help books."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-applehelp/sphinxcontrib-applehelp-1.0.1.tar.gz"
    git = "https://github.com/sphinx-doc/sphinxcontrib-applehelp.git"

    # 'sphinx' requires 'sphinxcontrib-applehelp' at build-time, but
    # 'sphinxcontrib-applehelp' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules for this package.
    import_modules: List[str] = []

    version("1.0.2", sha256="a072735ec80e7675e3f432fcae8610ecf509c5f1869d17e2eecff44389cdbc58")
    version("1.0.1", sha256="edaa0ab2b2bc74403149cb0209d6775c96de797dfd5b5e2a71981309efab3897")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
