# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyWids(PythonPackage):
    """High performance storage and I/O for deep learning and data processing."""

    homepage = "http://github.com/webdataset/webdataset"
    pypi = "wids/wids-0.1.11.tar.gz"

    license("BSD-3-Clause")
    maintainers("adamjstewart")

    version("0.1.11", sha256="b266230250f93396ee6075d76462d1087566819bdad48b194357dc8758d05eb9")

    depends_on("py-setuptools@45:", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:")
        depends_on("py-braceexpand")
        depends_on("py-numpy")
        depends_on("py-pyyaml")
