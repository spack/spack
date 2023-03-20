# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMaturin(PythonPackage):
    """Build and publish crates with pyo3, rust-cpython and cffi bindings
    as well as rust binaries as python packages.
    """

    homepage = "https://github.com/pyo3/maturin"
    pypi = "maturin/maturin-0.13.7.tar.gz"

    version("0.13.7", sha256="c0a77aa0c57f945649ca711c806203a1b6888ad49c2b8b85196ffdcf0421db77")

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel@0.36.2:", type="build")
    depends_on("py-setuptools-rust@1.4:", type="build")
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))
