# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyclibrary(PythonPackage):
    """C parser and bindings automation for Python."""

    homepage = "https://pyclibrary.readthedocs.io"
    pypi = "pyclibrary/pyclibrary-0.2.2.tar.gz"

    version("0.2.2", sha256="9902fffe361bb86f57ab62aa4195ec4dd382b63c5c6892be6d9784ec0a3575f7")

    depends_on("py-setuptools", type="build")
    depends_on("python", type=("build", "run"))
    depends_on("py-pyparsing@2.3.1:3", type=("build", "run"))
