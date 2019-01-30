# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Iperf2(AutotoolsPackage):
    """This code is a continuation based from the no longer maintained iperf
    2.0.5 code base. Iperf 2.0.5 is still widely deployed and used by many for
    testing networks and for qualifying networking products."""

    homepage = "https://sourceforge.net/projects/iperf2"
    url      = "https://downloads.sourceforge.net/project/iperf2/iperf-2.0.12.tar.gz"

    version('2.0.12', 'e501e26b9289097086ce0c44a42b10bc')
