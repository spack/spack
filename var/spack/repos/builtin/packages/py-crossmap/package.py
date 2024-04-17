# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCrossmap(PythonPackage, SourceforgePackage):
    """CrossMap is a program for convenient conversion of genome coordinates
    (or annotation files) between different assemblies"""

    homepage = "http://crossmap.sourceforge.net/"
    sourceforge_mirror_path = "crossmap/CrossMap-0.3.3.tar.gz"

    version(
        "0.3.9",
        sha256="99b18b1b663f40840536668bc0b962f1d7d3d03c29454f7b6cf7bd86a584ce07",
        url="https://pypi.org/packages/18/a5/d4302837a655ade7c53ee9fd6178a55077e918cc9dd23197ac010cd3e133/CrossMap-0.3.9-py3-none-any.whl",
    )
    version(
        "0.3.3",
        sha256="234710bf96482866686cacec46aac1229049ee827050f6991ce13bcbb3ea12da",
        url="https://pypi.org/packages/2f/8f/4beb4d8bb30144ef619cc7c3b7331e2b29e133fde10fb65561b1c2ab95cc/CrossMap-0.3.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-bx-python")
        depends_on("py-cython@0.17:", when="@:0.6")
        depends_on("py-pybigwig", when="@0.3:")
        depends_on("py-pysam")
