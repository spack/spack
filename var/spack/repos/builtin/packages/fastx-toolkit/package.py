# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FastxToolkit(AutotoolsPackage):
    """The FASTX-Toolkit is a collection of command line tools for
       Short-Reads FASTA/FASTQ files preprocessing."""

    homepage = "http://hannonlab.cshl.edu/fastx_toolkit/"
    url      = "https://github.com/agordon/fastx_toolkit/releases/download/0.0.14/fastx_toolkit-0.0.14.tar.bz2"

    version('0.0.14', 'bf1993c898626bb147de3d6695c20b40')

    depends_on('libgtextutils')

    # patch implicit fallthrough
    patch("pr-22.patch")
