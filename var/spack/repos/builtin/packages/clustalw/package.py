# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Clustalw(AutotoolsPackage):
    """Multiple alignment of nucleic acid and protein sequences."""

    homepage = "http://www.clustal.org/clustal2/"
    url      = "http://www.clustal.org/download/2.1/clustalw-2.1.tar.gz"

    version('2.1', '144df8440a0ae083d5167616c8ceeb41')
