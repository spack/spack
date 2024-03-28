# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPhylophlan(PythonPackage):
    """PhyloPhlAn 3.0 is an integrated pipeline for large-scale
    phylogenetic profiling of genomes and metagenomes."""

    homepage = "https://github.com/biobakery/phylophlan"
    url = "https://github.com/biobakery/phylophlan/archive/refs/tags/3.0.3.tar.gz"

    license("MIT")

    version(
        "3.0.3",
        sha256="1c37393742fa2eefb1f7b7829609d0dac03d53dae761c6ab2db13b4c4609cb79",
        url="https://pypi.org/packages/74/92/0513cefa30ef0f6bef6d7441bf59979213510efdbf875bc877521b5a96e9/PhyloPhlAn-3.0.3-py3-none-any.whl",
    )
    version(
        "3.0.2",
        sha256="1f5626a920aaed8f0e2ce333326945ea7267a096d7de5cc57dce785079618e16",
        url="https://pypi.org/packages/61/84/be11873e8749b1c5e5f914a65a23ce41d90204590044129f630516c14420/PhyloPhlAn-3.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-biopython", when="@3.0.1:")
        depends_on("py-dendropy", when="@3.0.1:")
        depends_on("py-matplotlib", when="@3.0.1:")
        depends_on("py-numpy", when="@3.0.1:")
        depends_on("py-pandas", when="@3.0.1:")
        depends_on("py-seaborn", when="@3.0.1:")
