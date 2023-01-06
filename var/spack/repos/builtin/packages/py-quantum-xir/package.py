# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQuantumXir(PythonPackage):
    """XIR is an intermediate representation language for quantum circuits."""

    homepage = "https://github.com/XanaduAI/xir"
    pypi = "quantum-xir/quantum-xir-0.2.1.tar.gz"

    version("0.2.1", sha256="9de3bbfdac5efd23e83fe5d62d5ea684a2e3e55af90269de03827bdbcd26bbfa")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-lark-parser@0.11.0:", type=("build", "run"))
