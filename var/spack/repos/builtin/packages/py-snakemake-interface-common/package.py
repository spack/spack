# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceCommon(PythonPackage):
    """Common functions and classes for Snakemake and its plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-common"
    pypi = "snakemake_interface_common/snakemake_interface_common-1.17.1.tar.gz"

    license("MIT")

    version(
        "1.17.1",
        sha256="2fdc4f2d778cad5284e83f35d1c2328b08cd6b8b9b29e522107f1a3c5ae771da",
        url="https://pypi.org/packages/6b/70/b6a53b63958dfa502ed498147d1e37a127d1be55ed2617a14047e79dcaf2/snakemake_interface_common-1.17.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3")
        depends_on("py-argparse-dataclass@2:")
        depends_on("py-configargparse@1.7:")
