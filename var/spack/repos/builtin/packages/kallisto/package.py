# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kallisto(CMakePackage):
    """kallisto is a program for quantifying abundances of transcripts from
       RNA-Seq data."""

    homepage = "http://pachterlab.github.io/kallisto"
    url      = "https://github.com/pachterlab/kallisto/archive/v0.43.1.tar.gz"

    version('0.43.1', sha256='7baef1b3b67bcf81dc7c604db2ef30f5520b48d532bf28ec26331cb60ce69400')

    depends_on('zlib')
    depends_on('hdf5')
    depends_on('mpich')
