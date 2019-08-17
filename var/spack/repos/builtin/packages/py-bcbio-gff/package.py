# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBcbioGff(PythonPackage):
    """Read and write Generic Feature Format (GFF) with Biopython
    integration."""

    homepage = "https://pypi.python.org/pypi/bcbio-gff/0.6.2"
    url      = "https://pypi.io/packages/source/b/bcbio-gff/bcbio-gff-0.6.2.tar.gz"

    version('0.6.2', 'd5aae8b125cdad4291f15bec20cfb0ef')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
    depends_on('py-biopython',  type=('build', 'run'))
