# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDebugpy(PythonPackage):
    """An implementation of the Debug Adapter Protocol for Python."""

    homepage = "https://github.com/microsoft/debugpy/"
    pypi = "debugpy/debugpy-1.4.1.zip"

    # 'debugpy._vendored' requires additional dependencies, Windows-specific
    skip_modules = ["debugpy._vendored"]

    version("1.6.3", sha256="e8922090514a890eec99cfb991bab872dd2e353ebb793164d5f01c362b9a40bf")
    version("1.5.1", sha256="d2b09e91fbd1efa4f4fda121d49af89501beda50c18ed7499712c71a4bf3452e")
    version("1.4.1", sha256="889316de0b8ff3732927cb058cfbd3371e4cd0002ecc170d34c755ad289c867c")

    depends_on("python@3.7:", when="@1.6:", type=("build", "link", "run"))
    depends_on("python@2.7:2.8,3.5:", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
