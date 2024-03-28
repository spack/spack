# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsUflLegacy(PythonPackage):
    """The Unified Form Language (UFL) is a domain specific language for
    declaration of finite element discretizations of variational forms. More
    precisely, it defines a flexible interface for choosing finite element
    spaces and defining expressions for weak forms in a notation close to
    mathematical notation."""

    homepage = "https://fenicsproject.org/"
    url = "https://github.com/FEniCS/ufl-legacy/archive/2022.3.0.tar.gz"
    git = "https://github.com/FEniCS/ufl-legacy.git"
    maintainers("chrisrichardson", "garth-wells", "jhale")

    license("LGPL-3.0-or-later")

    version(
        "2022.3.0",
        sha256="c909fcb4e837dd755b13541b274fe4c5e4147ce26c31e9dd209db36c3010f18f",
        url="https://pypi.org/packages/c4/ea/8de7b587715fb690ef872687eee8b9d39630af010adbd449d55053ac38ad/fenics_ufl_legacy-2022.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        with working_dir("test"):
            Executable("py.test")()
