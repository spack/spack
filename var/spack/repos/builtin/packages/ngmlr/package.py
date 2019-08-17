# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ngmlr(CMakePackage):
    """Ngmlr is a long-read mapper designed to align PacBilo or Oxford
       Nanopore to a reference genome with a focus on reads that span
       structural variations."""

    homepage = "https://github.com/philres/ngmlr"
    url      = "https://github.com/philres/ngmlr/archive/v0.2.5.tar.gz"

    version('0.2.5', '1b2b1aaeb6a3accc8b9f3e5c29e77037')
