# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *

# Package automatically generated using 'pip2spack' converter


class PyPymoo(PythonPackage):
    """
    Multi-Objective Optimization in Python
    """

    homepage = "https://pymoo.org"
    pypi = "pymoo/pymoo-0.5.0.tar.gz"
    maintainers("liuyangzhuan")

    license("Apache-2.0")

    version("0.6.1.3", sha256="ab440986cbaede547125ca9d1545781fdee94b719488de44119a86b8e9af526e")
    version("0.5.0", sha256="2fbca1716f6b45e430197ce4ce2210070fd3b6b9ec6b17bb25d98486115272c2")
    version("0.4.2", sha256="6ec382a7d29c8775088eec7f245a30fd384b42c40f230018dea0e3bcd9aabdf1")

    depends_on("cxx", type="build")  # generated

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-cython@0.29:", when="@0.6.1.3:")

    with default_args(type=("build", "run")):
        depends_on("python@3.4:")
        depends_on("py-autograd")

        with when("@0.6.1.3:"):
            depends_on("python@3.9:")
            depends_on("py-numpy@1.15:")
            depends_on("py-scipy@1.1:")
            depends_on("py-matplotlib@3:")
            depends_on("py-autograd@1.4:")
            depends_on("py-cma@3.2.2:")
            depends_on("py-alive-progress")
            depends_on("py-dill")
            depends_on("py-deprecated")
