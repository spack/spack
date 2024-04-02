# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonFsutil(PythonPackage):
    """file-system utilities for lazy devs."""

    homepage = "https://github.com/fabiocaccamo/python-fsutil"
    pypi = "python-fsutil/python-fsutil-0.4.0.tar.gz"

    license("MIT")

    version(
        "0.4.0",
        sha256="3e93c919b96a146de78900b644c9d9f957b1d50ae67c510a39f866d30ab626c7",
        url="https://pypi.org/packages/4b/b1/d9cd591b718300a3c45d959bd71c87cbac932a906d5efc20892e5d152e67/python_fsutil-0.4.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-requests", when="@0.4:0.5")
