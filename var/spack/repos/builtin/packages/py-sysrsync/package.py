# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySysrsync(PythonPackage):
    """Python module that wraps system calls to rsync."""

    pypi = "sysrsync/sysrsync-1.1.1.tar.gz"

    license("MIT")

    version(
        "1.1.1",
        sha256="9c8877f162dce9c480804445fca56cd19bf41b998d2172651468ccebfdc60850",
        url="https://pypi.org/packages/ce/82/5939e68632beebdb6f61a52246c0243e8490d9f75e0f1a214dda0113d5f2/sysrsync-1.1.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@0.2:")
        depends_on("py-toml@0.10:", when="@0.2:")
