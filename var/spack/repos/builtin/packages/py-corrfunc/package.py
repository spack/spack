# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCorrfunc(PythonPackage):
    """Blazing fast correlation functions on the CPU."""

    homepage = "https://corrfunc.readthedocs.io/"
    pypi = "corrfunc/corrfunc-2.5.3.tar.gz"

    maintainers("lgarrison")

    license("MIT", checked_by="lgarrison")

    version("2.5.3", sha256="32836235e2389f55f028664231f0d6f5716ac0d4226c620c0bbac9407dc225a1")

    depends_on("c", type="build")

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("gmake", type="build")

    depends_on("py-numpy@1.20:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-wurlitzer", type=("build", "run"))

    depends_on("gsl@2.4:", type=("build", "link"))

    def patch(self):
        filter_file(r"^\s*CC\s*[:\?]?=.*", f"CC := {spack_cc}", "common.mk")
        filter_file("-march=native", "", "common.mk")
