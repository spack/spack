# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rsync(AutotoolsPackage):
    """An open source utility that provides fast incremental file transfer."""
    homepage = "https://rsync.samba.org"
    url      = "https://download.samba.org/pub/rsync/src/rsync-3.1.2.tar.gz"

    version('3.1.3', '1581a588fde9d89f6bc6201e8129afaf')
    version('3.1.2', '0f758d7e000c0f7f7d3792610fad70cb')
    version('3.1.1', '43bd6676f0b404326eee2d63be3cdcfe')
