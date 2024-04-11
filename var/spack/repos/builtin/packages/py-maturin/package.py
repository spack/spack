# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

    license("Apache-2.0")

    version("1.4.0", sha256="ed12e1768094a7adeafc3a74ebdb8dc2201fa64c4e7e31f14cfc70378bf93790")
    version("1.1.0", sha256="4650aeaa8debd004b55aae7afb75248cbd4d61cd7da2dcf4ead8b22b58cecae0")
    version("0.14.17", sha256="fb4e3311e8ce707843235fbe8748a05a3ae166c3efd6d2aa335b53dfc2bd3b88")
    version("0.13.7", sha256="c0a77aa0c57f945649ca711c806203a1b6888ad49c2b8b85196ffdcf0421db77")

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel@0.36.2:", type="build")
    depends_on("py-setuptools-rust@1.4:", type="build")
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))
    depends_on("rust", type=("build", "run"))
