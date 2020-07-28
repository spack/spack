# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dire(Package):
    """DIRE (short for dipole resummation) a C++ program for all-order
    radiative corrections to scattering processes in high-energy particle
    collisions."""

    homepage = "http://dire.gitlab.io/"
    url      = "http://dire.gitlab.io/Downloads/DIRE-2.004.tar.gz"
    git      = "http://gitlab.com/dire/direforpythia"
    list_url = "http://dire.gitlab.io/Downloads.html"

    maintainer = ['mdiefent']

    version('2.004', sha256='8cc1213b58fec744fdaa50834560a14b141de99efb2c3e3d3d47f3d6d84b179f')
    version('2.003', sha256='98ee082718504c0f514a5c377310c4a2a34bb9625c999d3690d92342e52b532a')
    version('2.002', sha256='7fba480bee785ddacd76446190df766d74e61a3c5969f362b8deace7d3fed8c1')
    version('2.001', sha256='d9d5f8ff6829c51fefc008a78f4fa0ac3f4be99cd2a03ef01ca9fb84f4319836')
    version('2.000', sha256='ce30477474709496d3c9a31806c12872fb003cdeec412ec4027245da6aa8b40b')
    version('1.500', sha256='3b6e711a8b161e60f84168a3560bf71b3cf89f566f3b536631208e475fdc512f')

    depends_on('zlib')
    depends_on('boost')
    depends_on('lhapdf')
    depends_on('hepmc')
    depends_on('pythia8@8212:', when='@:2.000')
    depends_on('pythia8@8226:', when='@2.001:')

    def install(self, spec, prefix):
        configure_args = ['--prefix={0}'.format(prefix)]
        configure_args.append(
            '--with-pythia8={0}'.format(spec['pythia8'].prefix))
        configure(*configure_args)
        make()
        # Open bug: https://gitlab.com/wdconinc/direforpythia/-/merge_requests/1
        filter_file('-Wl,-rpath ', '-Wl,-rpath,', 'bin/dire-config')
        make('install')
