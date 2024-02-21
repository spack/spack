# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceCommon(PythonPackage):
    """Common functions and classes for Snakemake and its plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-common"
    pypi = "snakemake_interface_common/snakemake_interface_common-1.17.0.tar.gz"

    license("MIT")

    version("1.17.0", sha256="d1f0cb83611f24f62ec5af852cee1cef429dd4e86c55bf373092fc682acac133")

    depends_on("py-argparse-dataclass@2", type=("build", "run"))
    depends_on("py-configargparse@1.7:1", type=("build", "run"))

    depends_on("python@:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
