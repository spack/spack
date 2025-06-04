# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCppy(PythonPackage):
    """C++ headers for C extension development"""

    homepage = "https://github.com/nucleic/cppy"
    pypi = "cppy/cppy-1.1.0.tar.gz"

    license("BSD-3-Clause")

    version("1.3.1", sha256="55b5307c11874f242ea135396f398cb67a5bbde4fab3e3c3294ea5fce43a6d68")
    version("1.3.0", sha256="da7413a286d5d31626ba35ed2c70ddfb033520cc81310088ba5a57d34039f604")
    version("1.2.1", sha256="83b43bf17b1085ac15c5debdb42154f138b928234b21447358981f69d0d6fe1b")
    version("1.1.0", sha256="4eda6f1952054a270f32dc11df7c5e24b259a09fddf7bfaa5f33df9fb4a29642")

    depends_on("py-setuptools@61.2:", when="@1.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm+toml@3.4.3:", when="@1.2:", type="build")
