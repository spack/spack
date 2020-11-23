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

    tags = ['hep']

    maintainer = ['mdiefent']

    version('2.004', sha256='8cc1213b58fec744fdaa50834560a14b141de99efb2c3e3d3d47f3d6d84b179f')

    depends_on('zlib')
    depends_on('boost')
    depends_on('lhapdf')
    depends_on('hepmc')
    depends_on('pythia8@8226:8244')

    def install(self, spec, prefix):
        configure_args = ['--prefix={0}'.format(prefix)]
        configure_args.append(
            '--with-pythia8={0}'.format(spec['pythia8'].prefix))
        configure(*configure_args)
        make()
        # Open bug: https://gitlab.com/wdconinc/direforpythia/-/merge_requests/1
        filter_file('-Wl,-rpath ',
                    self.compiler.cc_rpath_arg,
                    'bin/dire-config')
        make('install')
