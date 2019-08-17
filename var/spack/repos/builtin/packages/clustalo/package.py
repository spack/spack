# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Clustalo(AutotoolsPackage):
    """Clustal Omega: the last alignment program you'll ever need."""

    homepage = "http://www.clustal.org/omega/"
    url      = "http://www.clustal.org/omega/clustal-omega-1.2.4.tar.gz"

    version('1.2.4', '6c0459f4c463a30e942ce7e0efc91422')

    depends_on('argtable')
