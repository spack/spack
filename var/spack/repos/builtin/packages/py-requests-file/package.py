# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsFile(PythonPackage):
    """File transport adapter for Requests."""

    homepage = "http://github.com/dashea/requests-file"
    pypi = "requests-file/requests-file-1.5.1.tar.gz"

    maintainers("LydDeb")

    license("Apache-2.0")

    version(
        "1.5.1",
        sha256="dfe5dae75c12481f68ba353183c53a65e6044c923e64c24b2209f6c7570ca953",
        url="https://pypi.org/packages/77/86/cdb5e8eaed90796aa83a6d9f75cfbd37af553c47a291cd47bc410ef9bdb2/requests_file-1.5.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-requests@1:", when="@1.5:")
        depends_on("py-six", when="@1.5:1")
