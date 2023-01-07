# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQuantumXir(PythonPackage):
    """XIR is an intermediate representation language for quantum circuits."""

    homepage = "https://github.com/XanaduAI/xir"
    url = "https://github.com/XanaduAI/xir/archive/refs/tags/v0.2.1.tar.gz"
    # using github for now, because pypi tarball is missing the requirements.txt file
    # pypi = "quantum-xir/quantum-xir-0.2.1.tar.gz"

    version("0.2.1", sha256="bfc28ff386a4a742973455b61eccc574517a994bb7cfd0ea0b9e7194dae55f31")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-lark-parser@0.11.0:", type=("build", "run"))
