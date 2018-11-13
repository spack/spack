# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bwtool(AutotoolsPackage):
    """bwtool is a command-line utility for bigWig files."""

    homepage = "https://github.com/CRG-Barcelona/bwtool"
    url      = "https://github.com/CRG-Barcelona/bwtool/archive/1.0.tar.gz"

    version('1.0', 'cdd7a34ae457b587edfe7dc8a0bdbedd')

    depends_on('libbeato')
