# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Smalt(AutotoolsPackage):
    """SMALT aligns DNA sequencing reads with a reference genome."""

    homepage = "http://www.sanger.ac.uk/science/tools/smalt-0"
    url      = "https://downloads.sourceforge.net/project/smalt/smalt-0.7.6.tar.gz"

    version('0.7.6', sha256='89ccdfe471edba3577b43de9ebfdaedb5cd6e26b02bf4000c554253433796b31')
