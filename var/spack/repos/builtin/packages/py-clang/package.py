# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyClang(PythonPackage):
    """Python bindings for clang from clang release branches"""

    # This package is needed for py-tensorflow@2.6. Generally speaking the
    # py-libclang package should be used instead. It not recommended to add
    # updated versions to this package. Note that no llvm dependency is
    # specified here because llvm-5 will cause spack concretization to use an
    # equally old GCC.

    homepage = "https://clang.llvm.org/"
    pypi = "clang/clang-5.0.tar.gz"

    version(
        "5.0", sha256="ceccae97eda0225a5b44d42ffd61102e248325c2865ca53e4407746464a5333a"
    )

    depends_on("python@2.7:2.8,3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
