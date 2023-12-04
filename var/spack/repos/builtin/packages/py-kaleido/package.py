# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class PyKaleido(PythonPackage):
    """Static image export for web-based visualization libraries with zero dependencies"""

    homepage = "https://github.com/wdecoster/nanostat"
    pypi = "kaleido/kaleido-0.2.1.post1-py2.py3-none-manylinux2014_armv7l.whl"

    maintainers("Pandapip1")

    version("0.2.1", sha256="d313940896c24447fc12c74f60d46ea826195fc991f58569a6e73864d53e5c20")

    depends_on("python@:3.4")
