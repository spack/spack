# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Iperf3(AutotoolsPackage):
    """The iperf series of tools perform active measurements to determine the
    maximum achievable bandwidth on IP networks. iperf2 is a separately
    maintained project."""

    homepage = "https://software.es.net/iperf/"
    url      = "https://github.com/esnet/iperf/archive/3.6.tar.gz"

    version('3.6', '5082ffc4141abc1bac7cbd59337ff409')
