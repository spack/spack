# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPacificaNamespace(PythonPackage):
    """Python Pacifica Namespace Library"""

    homepage = "https://github.com/pacifica/pacifica-namespace/"
    pypi = "pacifica-namespace/pacifica-namespace-0.0.2.tar.gz"

    license("LGPL-3.0-only")

    version(
        "0.0.2",
        sha256="6b1d9992a839cf84ef8f5568cd323d16dc420aed7a61257e76717980ecea3b1b",
        url="https://pypi.org/packages/28/3b/2282a452b35cdbc21796de63d7dd7bdf63bb8e878e2835989e8cf23b6a42/pacifica_namespace-0.0.2-py3-none-any.whl",
    )
