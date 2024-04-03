# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyStrawberryfields(PythonPackage):
    """Open source library for continuous-variable quantum computation"""

    homepage = "https://github.com/XanaduAI/StrawberryFields"
    pypi = "StrawberryFields/StrawberryFields-0.23.0.tar.gz"

    maintainers("marcodelapierre")

    license("Apache-2.0")

    version(
        "0.23.0",
        sha256="3298b77b07e5e8e16e63af253ac20b826a9df926f8002450ea421e7c9faaeac7",
        url="https://pypi.org/packages/c0/16/e0062ed6fb37bc3734660aed2a4ddbef0cfd82b78dae48b82e9aa2019075/StrawberryFields-0.23.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-networkx@2:")
        depends_on("py-numba")
        depends_on("py-numpy@1.17.4:")
        depends_on("py-python-dateutil@2.8:")
        depends_on("py-quantum-blackbird@0.3:", when="@0.17:")
        depends_on("py-quantum-xir@0.1.1:", when="@0.21:")
        depends_on("py-requests@2.22:")
        depends_on("py-scipy@1.0.0:")
        depends_on("py-sympy@1.5:")
        depends_on("py-thewalrus@0.18:", when="@0.21:")
        depends_on("py-toml")
        depends_on("py-urllib3@1.25.3:")
        depends_on("py-xanadu-cloud-client@0.2.1:", when="@0.23:")
