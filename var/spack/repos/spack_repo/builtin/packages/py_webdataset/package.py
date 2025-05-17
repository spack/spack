# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyWebdataset(PythonPackage):
    """Python-based I/O for deep learning problems."""

    homepage = "https://github.com/webdataset/webdataset"
    pypi = "webdataset/webdataset-0.1.62.tar.gz"

    license("BSD-3-Clause")
    maintainers("adamjstewart")

    version("0.2.111", sha256="5b2835386a25601307a9ded9bcc0dbd1e81a9eee017784152528e77dd8619511")
    version("0.1.62", sha256="78b6c7810116d6875fa1ed8eb2dea29a54b86fde014cc2069f4c08fc3530ceb5")

    depends_on("py-setuptools@45:", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:")
        depends_on("py-braceexpand")
        depends_on("py-numpy")
        depends_on("py-pyyaml")
