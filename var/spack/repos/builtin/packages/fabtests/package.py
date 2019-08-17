# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fabtests(AutotoolsPackage):
    """Fabtests provides a set of examples that uses libfabric.

    DEPRECATED. Fabtests has merged with the libfabric git repo."""

    homepage = "http://libfabric.org"
    url      = "https://github.com/ofiwg/fabtests/releases/download/v1.5.3/fabtests-1.5.3.tar.gz"

    version('1.6.0', '0441aa0aeda391b1bf1eb71250a4afbc')
    version('1.5.3', 'f60cb95843ebf62e4eaa128e08ccdc7d')

    depends_on('libfabric@1.6.0', when='@1.6.0')
    depends_on('libfabric@1.5.3', when='@1.5.3')
