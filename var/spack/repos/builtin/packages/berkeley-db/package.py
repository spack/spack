# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BerkeleyDb(AutotoolsPackage):
    """Oracle Berkeley DB"""

    homepage = "http://www.oracle.com/technetwork/database/database-technologies/berkeleydb/overview/index.html"
    url      = "http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz"

    version('5.3.28', 'b99454564d5b4479750567031d66fe24')
    version('6.0.35', 'c65a4d3e930a116abaaf69edfc697f25')
    version('6.1.29', '7f4d47302dfec698fe088e5285c9098e')
    version('6.2.32', '33491b4756cb44b91c3318b727e71023')

    configure_directory = 'dist'
    build_directory = 'spack-build'

    def url_for_version(self, version):
        # newer version need oracle login, so get them from gentoo mirror
        return 'http://distfiles.gentoo.org/distfiles/db-{0}.tar.gz'.format(version)

    def configure_args(self):
        return ['--disable-static', '--enable-cxx', '--enable-stl']
