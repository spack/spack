# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyJustext(PythonPackage):
    """Heuristic based boilerplate removal tool."""

    homepage = "https://github.com/miso-belica/jusText"
    pypi = "justext/justext-3.0.2.tar.gz"

    version("3.0.2", sha256="13496a450c44c4cd5b5a75a5efcd9996066d2a189794ea99a49949685a0beb05")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-lxml@4.4.2:", type=("build", "run"))
