# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyLitdata(PythonPackage):
    """The Deep Learning framework to train, deploy, and ship AI products Lightning fast."""

    homepage = "https://github.com/Lightning-AI/litdata"
    pypi = "litdata/litdata-0.2.44.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("0.2.44", sha256="0c2ad485d4692702d97a396bfe6017f9ac2af2832bb39fae99fd49c26e207a0e")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-torch")
        depends_on("py-filelock")
        depends_on("py-numpy")
        depends_on("py-boto3")
        depends_on("py-requests")
        depends_on("py-tifffile")
