# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsFfc(PythonPackage):
    """The FEniCS Form Compiler FFC is a compiler for finite element
    variational forms, translating high-level mathematical descriptions
    of variational forms into efficient low-level C++ code for finite
    element assembly."""

    homepage = "https://fenicsproject.org/"
    git = "https://bitbucket.org/fenics-project/ffc.git"
    url = "https://bitbucket.org/fenics-project/ffc/downloads/ffc-2019.1.0.post0.tar.gz"
    maintainers("emai-imcs")

    license("LGPL-3.0-or-later")
    version(
        "2019.1.0.post0",
        sha256="54d7529ca6306f32e15e8e4a26f32a3d2ec68902262191148b32c92657a6851f",
        url="https://pypi.org/packages/74/b6/0c3743a5b9fecaf3b7fe7b0c6526e7c635bd1bb6f9bc4a177bababc79131/fenics_ffc-2019.1.0.post0-py3-none-any.whl",
    )
    version(
        "2018.1.0",
        sha256="d81df998e6aa244b40211727347cdaf621a26a9a9106ce301ac9b91b6fdd485a",
        url="https://pypi.org/packages/01/d2/787ac08eaf2bb074d80269cea5d35d337892b8d4d879e02419a614f6c100/fenics_ffc-2018.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-fenics-dijitso@2019:", when="@2019:")
        depends_on("py-fenics-dijitso@2018", when="@2018")
        depends_on("py-fenics-fiat@2019:", when="@2019:")
        depends_on("py-fenics-fiat@2018", when="@2018")
        depends_on("py-fenics-ufl@2019", when="@2019:")
        depends_on("py-fenics-ufl@2018", when="@2018")
        depends_on("py-numpy", when="@2018:")
