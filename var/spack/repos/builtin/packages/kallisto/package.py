# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kallisto(CMakePackage):
    """kallisto is a program for quantifying abundances of transcripts from
       RNA-Seq data."""

    homepage = "http://pachterlab.github.io/kallisto"
    url      = "https://github.com/pachterlab/kallisto/archive/v0.43.1.tar.gz"

    version('0.43.1', '071e6bfb62be06fd76552298d4cf8144')

    depends_on('zlib')
    depends_on('hdf5')
    depends_on('mpich')
