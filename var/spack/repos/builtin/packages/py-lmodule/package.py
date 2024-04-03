# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLmodule(PythonPackage):
    """Lmodule is a Python API for Lmod module system. It's primary purpose is
    to help automate module testing. Lmodule uses Lmod spider tool to query
    all modules in-order to automate module testing. Lmodule can be used with
    environment-modules to interact with module using the Module class."""

    homepage = "https://lmodule.readthedocs.io/en/latest/"
    pypi = "lmodule/lmodule-0.1.0.tar.gz"
    git = "https://github.com/buildtesters/lmodule"

    maintainers("shahzebsiddiqui")

    license("MIT")

    version(
        "0.1.0",
        sha256="2584138a3ecbe430d777f9ba194b099041649e78ea6619eeee0b8133ca796244",
        url="https://pypi.org/packages/58/aa/28b051d38a02a5ca4abbeb8bbbecee7e7ea538d031bc77b626deff08d77d/lmodule-0.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3")
