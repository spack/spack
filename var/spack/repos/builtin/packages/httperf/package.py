# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Httperf(AutotoolsPackage):
    """Httperf is a tool for measuring web server performance. It provides
    a flexible facility for generating various HTTP workloads and for
    measuring server performance."""

    homepage = "https://github.com/httperf"
    url      = "https://github.com/httperf/httperf/archive/master.zip"

    version('master', 'e9fb12a3b3462ec8bc354c886890cdf9')

    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('m4')

    @run_before('autoreconf')
    def e_autogen(self):
        mkdirp('m4')
