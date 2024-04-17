# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestSubprocess(PythonPackage):
    """A plugin to fake subprocess for pytest."""

    homepage = "https://pytest-subprocess.readthedocs.io/en/latest/"
    pypi = "pytest-subprocess/pytest-subprocess-1.5.0.tar.gz"
    git = "https://github.com/aklajnert/pytest-subprocess"

    maintainers("wdconinc")

    license("MIT")

    version(
        "1.5.0",
        sha256="dfd75b10af6800a89a9b758f2e2eceff9de082a27bd1388521271b6e8bde298b",
        url="https://pypi.org/packages/44/96/de22cf4a31bf5f21e6b74dc57e3628e3bc78847acf7a1752bdb1e36dfaf1/pytest_subprocess-1.5.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pytest@4:")
