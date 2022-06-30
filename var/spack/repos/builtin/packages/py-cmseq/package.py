# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCmseq(PythonPackage):
    """CMSeq is a set of commands to provide an
       interface to .bam files for coverage and sequence
       consensus. Used as a dependency for py-metaphlan."""

    homepage = "https://github.com/SegataLab/cmseq"
    url      = "https://github.com/SegataLab/cmseq/archive/refs/tags/1.0.4.tar.gz"

    version('1.0.4', sha256='9d9412b0c58dfaef0d9e3621a0c4b7cd5330dbc1399370d3e69ba03959a26d68')

    depends_on('py-numpy')
    depends_on('samtools@1.2:')
    depends_on('py-pysam')
    depends_on('py-pandas')
    depends_on('py-biopython@:1.76')
    depends_on('py-setuptools@:57', type=('build'))
