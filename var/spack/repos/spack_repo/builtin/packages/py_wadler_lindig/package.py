# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyWadlerLindig(PythonPackage):
    """A Wadler–Lindig pretty-printer for Python"""

    homepage = "https://docs.kidger.site/wadler_lindig"
    pypi = "wadler_lindig/wadler_lindig-0.1.3.tar.gz"

    version("0.1.3", sha256="476fb7015135f714cef8f8eac7c44b164c8b993345e651a9b6f25b7b112440c9")

    maintainers("viperML")

    license("Apache-2.0", checked_by="viperML")

    depends_on("py-hatchling", type="build")
    depends_on("python@3.10:", type=("build", "run"))
