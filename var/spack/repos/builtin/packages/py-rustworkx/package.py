# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRustworkx(PythonPackage):
    """Rustworkx was originally called retworkx and was was created initially to
    be a replacement for qiskit's previous (and current) networkx usage (hence
    the original name). The project was originally started to build a faster
    directed graph to use as the underlying data structure for the DAG at the
    center of qiskit-terra's transpiler. However, since it's initial
    introduction the project has grown substantially and now covers all
    applications that need to work with graphs which includes Qiskit."""

    homepage = "https://github.com/Qiskit/rustworkx"
    pypi = "rustworkx/rustworkx-0.12.1.tar.gz"

    license("Apache-2.0")

    version("0.12.1", sha256="13a19a2f64dff086b3bffffb294c4630100ecbc13634b4995d9d36a481ae130e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-rust", type="build")
    depends_on("py-numpy@1.16:", type=("build", "run"))
