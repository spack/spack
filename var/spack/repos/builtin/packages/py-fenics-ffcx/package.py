# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsFfcx(PythonPackage):
    """Next generation FEniCS Form Compiler"""

    homepage = "https://github.com/FEniCS/ffcx"
    url = "https://github.com/FEniCS/ffcx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/ffcx.git"
    maintainers("chrisrichardson", "garth-wells", "jhale")

    license("LGPL-3.0-or-later")

    version(
        "0.7.0",
        sha256="638232b92d289a28d9722959ec3ecd88a771d6ae856a4129b17206cbfe91401a",
        url="https://pypi.org/packages/88/d2/341aa6c6f3345bcc0320c0dcde63bbbe41bc7bbd27a808aeed2e797fb167/fenics_ffcx-0.7.0-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="07afc04553e0822955a1eff85e1e1c73fa697ac79bc96c132353cb6a6d9ba9c6",
        url="https://pypi.org/packages/76/5f/a3b446ddfd8cd19098dbad83514ed0657852b74f34aee512fc7c5e8ec7c1/fenics_ffcx-0.6.0-py3-none-any.whl",
    )
    version(
        "0.5.0.post0",
        sha256="bc080e2529526c8448507ef51d9fd5119f30139b86049ab66a5d2097cd5a6282",
        url="https://pypi.org/packages/23/a6/d5de266501eb487949d57b2005a396f792bc3793398ce876326c771a0144/fenics_ffcx-0.5.0.post0-py3-none-any.whl",
    )
    version(
        "0.4.2",
        sha256="c83b6c52af80e14e09e7f77fe7c52a97d4186dd523a9f3629afffb0b991fe503",
        url="https://pypi.org/packages/6c/12/c2b66b33a55f36ee17685aea5198a346a34a71acc3a6eafada7f66163a64/fenics_ffcx-0.4.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cffi")
        depends_on("py-fenics-basix@0.7:", when="@0.7:")
        depends_on("py-fenics-basix@0.6", when="@0.6")
        depends_on("py-fenics-basix@0.5", when="@0.5")
        depends_on("py-fenics-basix@0.4.2:0.4", when="@0.4.2:0.4")
        depends_on("py-fenics-ufl@2023.2:", when="@0.7:")
        depends_on("py-fenics-ufl@2023:2023.1", when="@0.6")
        depends_on("py-fenics-ufl@2022.2:2022", when="@0.5")
        depends_on("py-fenics-ufl@2022:2022.1", when="@:0.4")
        depends_on("py-numpy")
        depends_on("py-setuptools", when="@0.5:")

    # Runtime dependency on pkg_resources from setuptools at 0.6.0

    # CFFI is required at runtime for JIT support
    # py-numpy>=1.21 required because FFCx uses NumPy typing (version
    # requirement not properly set in the FFCx pyproject.toml file)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        with working_dir("test"):
            pytest = which("pytest")
            pytest("--ignore=test_cmdline.py")
