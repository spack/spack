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

    version('master', '8a14602560914710a4caac56607d74ed82081ba0f666e3da903514eaac28c455')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    @run_before('autoreconf')
    def e_autogen(self):
        mkdirp('m4')
