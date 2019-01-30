# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Netgauge(AutotoolsPackage):
    """Netgauge is a high-precision network parameter measurement
    tool. It supports benchmarking of many different network protocols
    and communication patterns. The main focus lies on accuracy,
    statistical analysis and easy extensibility.
    """
    homepage = "http://unixer.de/research/netgauge/"
    url      = "http://unixer.de/research/netgauge/netgauge-2.4.6.tar.gz"

    version('2.4.6', 'e0e040ec6452e93ca21ccc54deac1d7f')

    depends_on("mpi")
