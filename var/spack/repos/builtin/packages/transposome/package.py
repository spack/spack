# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Transposome(PerlPackage):
    """A toolkit for annotation of transposable element families from
       unassembled sequence reads."""

    homepage = "https://sestaton.github.io/Transposome/"
    url      = "https://github.com/sestaton/Transposome/archive/v0.11.2.tar.gz"

    version('0.12.1', sha256='fc3706a883cba58626ccd753df7a77f0baf52ff3b1d8aa7644a7f474f296a603')
    version('0.12.0', sha256='a9fa49360f7e7ac49c350d1837d9804550048b1bab90202c3e19edebdacfe5e3')
    version('0.11.4', sha256='2e27bee4bde153d19dcd2ee439aa9c0253b9d9097ef3b8583caf489d4aeecdb4')
    version('0.11.3', sha256='d247b3af22c75048750031886f9e795376382798a1903746a2a7d62b2a1d3181')
    version('0.11.2', sha256='f0bfdb33c34ada726b36c7b7ed6defa8540a7f8abe08ad46b3ccfec5dcd4720d')

    depends_on('blast-plus')
