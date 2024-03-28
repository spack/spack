# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTblib(PythonPackage):
    """Traceback fiddling library. Allows you to pickle tracebacks."""

    homepage = "https://github.com/ionelmc/python-tblib"
    pypi = "tblib/tblib-1.6.0.tar.gz"

    license("BSD-2-Clause")

    version(
        "1.6.0",
        sha256="e222f44485d45ed13fada73b57775e2ff9bd8af62160120bbb6679f5ad80315b",
        url="https://pypi.org/packages/0d/de/dca3e651ca62e59c08d324f4a51467fa4b8cbeaafb883b5e83720b4d4a47/tblib-1.6.0-py2.py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="49188d1ed69938811e654a8f6e6a3cfca8a578d8fa95318d8a9861c7f4fccd19",
        url="https://pypi.org/packages/64/b5/ebb1af4d843047ccd7292b92f5e5f8643153e8b95d14508d9fe3b35f7004/tblib-1.4.0-py2.py3-none-any.whl",
    )
