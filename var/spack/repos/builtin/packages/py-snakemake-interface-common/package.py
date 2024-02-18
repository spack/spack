# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceCommon(PythonPackage):
    """Common functions and classes for Snakemake and its plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-common"
    pypi = "snakemake_interface_common/snakemake_interface_common-1.16.0.tar.gz"

    license("MIT")

    version("1.16.0", sha256="b0780b9c3525435031815fd1f01079828d55c83fef18b5a0b05caa965408046b")

    depends_on("py-argparse-dataclass@2", type=("build", "run"))
    depends_on("py-configargparse@1.7:1", type=("build", "run"))

    depends_on("python@:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
