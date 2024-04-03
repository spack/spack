# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyh5md(PythonPackage):
    """Read and write H5MD files."""

    homepage = "https://github.com/pdebuyl/pyh5md"
    pypi = "pyh5md/pyh5md-1.0.0.tar.gz"

    version(
        "1.0.0",
        sha256="0a3e80a20ff7662ffdfff0e6bd977e5cbabe3e3384d875ad3fb29455ecac75f9",
        url="https://pypi.org/packages/af/2b/7fc991000683111184a7d9882233b992104f4d8b62b4a31af3bab6fa628b/pyh5md-1.0.0-py2.py3-none-any.whl",
    )
