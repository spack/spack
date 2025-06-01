# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCourlan(PythonPackage):
    """Clean, filter and sample URLs to optimize data collection:
    deduplication, spam, content and language filters."""

    homepage = "https://github.com/adbar/courlan"
    pypi = "courlan/courlan-1.3.2.tar.gz"

    version("1.3.2", sha256="0b66f4db3a9c39a6e22dd247c72cfaa57d68ea660e94bb2c84ec7db8712af190")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-babel@2.16:", type=("build", "run"))
    depends_on("py-tld@0.13:", type=("build", "run"))
    depends_on("py-urllib3@1.26:2", type=("build", "run"))
