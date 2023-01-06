# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQuantumBlackbird(PythonPackage):
    """Blackbird is a quantum assembly language for continuous-variable quantum
    computation, that can be used to program Xanadu’s quantum photonics
    hardware and Strawberry Fields simulator.
    """

    homepage = ""
    pypi = "quantum-blackbird/"

    version("", sha256="")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("", type=("build", "run"))

    depends_on("", type="run")
