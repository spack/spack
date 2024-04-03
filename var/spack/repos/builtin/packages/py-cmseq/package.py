# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCmseq(PythonPackage):
    """CMSeq is a set of commands to provide an interface
    to .bam files for coverage and sequence consensus."""

    homepage = "https://github.com/SegataLab/cmseq"
    pypi = "CMSeq/CMSeq-1.0.4.tar.gz"

    license("MIT")

    version(
        "1.0.4",
        sha256="7165869f81ad668a94dd1f1dd243aedb1bccc50f1547f67355737d9570954d73",
        url="https://pypi.org/packages/5c/2f/0d4effb9b71f4b78ad4fc0d4e5d433cfb2a6bbf1b26ba2c4164be352b7c0/CMSeq-1.0.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-bcbio-gff", when="@1.0.2:")
        depends_on("py-biopython", when="@1.0.2:")
        depends_on("py-numpy", when="@1.0.2:")
        depends_on("py-pandas", when="@1.0.2:")
        depends_on("py-pysam", when="@1.0.2:")
        depends_on("py-scipy", when="@1.0.2:")
