# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDendropy(PythonPackage):
    """DendroPy is a Python library for phylogenetic computing. It provides
    classes and functions for the simulation, processing, and manipulation of
    phylogenetic trees and character matrices, and supports the reading and
    writing of phylogenetic data in a range of formats, such as NEXUS, NEWICK,
    NeXML, Phylip, FASTA, etc."""

    homepage = "https://www.dendropy.org"
    url      = "https://pypi.io/packages/source/d/dendropy/DendroPy-4.3.0.tar.gz"

    version('4.3.0',  '56c37eb7db69686c8ef3467562f4e7c5')
    version('3.12.0', '6971ac9a8508b4198fd357fab0affc84')

    depends_on('python@2.7:,3.4:')
    depends_on('py-setuptools', type='build')
