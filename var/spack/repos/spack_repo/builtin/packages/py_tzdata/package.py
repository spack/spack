# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTzdata(PythonPackage):
    """Provider of IANA time zone data."""

    homepage = "https://github.com/python/tzdata"
    pypi = "tzdata/tzdata-2023.3.tar.gz"

    license("Apache-2.0")

    version("2025.2", sha256="b60a638fcc0daffadf82fe0f57e53d06bdec2f36c4df66280ae79bce6bd6f2b9")
    version("2023.3", sha256="11ef1e08e54acb0d4f95bdb1be05da659673de4acbd21bf9c69e94cc5e907a3a")

    depends_on("py-setuptools@40.8:", type="build")
