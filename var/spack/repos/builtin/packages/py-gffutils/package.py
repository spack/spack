# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGffutils(PythonPackage):
    """GFF and GTF file manipulation and interconversion

    gffutils is a Python package for working with and manipulating the GFF and
    GTF format files typically used for genomic annotations. Files are loaded
    into a sqlite3 database, allowing much more complex manipulation of
    hierarchical features (e.g., genes, transcripts, and exons) than is
    possible with plain-text methods alone."""

    homepage = "https://github.com/daler/gffutils"
    url      = "https://github.com/daler/gffutils/archive/refs/tags/v0.10.1.tar.gz"

    maintainers = ['dorton21']

    version('0.10.1', sha256='c020f38d572a38227d575ca6b4a6781e10317c4231c7008f533bb6d9167f64d8')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyfaidx@0.5.5.2:', type=('build', 'run'))
    depends_on('py-six@1.12.0:', type=('build', 'run'))
    depends_on('py-argh@0.26.2:', type=('build', 'run'))
    depends_on('py-argcomplete@1.9.4:', type=('build', 'run'))
    depends_on('py-simplejson', type=('build', 'run'))
