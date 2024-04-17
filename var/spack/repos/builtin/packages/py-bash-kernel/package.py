# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBashKernel(PythonPackage):
    """A Jupyter kernel for bash."""

    homepage = "https://github.com/takluyver/bash_kernel"
    pypi = "bash_kernel/bash_kernel-0.7.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.7.2",
        sha256="4036f8c3bbd8a8570cb7b71a891e94b5cf5425c13467df879468a0e9b551b6b2",
        url="https://pypi.org/packages/5e/17/5e059b2cd785f111b9b1be53ac27000dbbd66291e778f9acf59371a8c541/bash_kernel-0.7.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pexpect@4:", when="@0.5:")
