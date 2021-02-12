# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dash(AutotoolsPackage):
    """The Debian Almquist Shell."""

    homepage = "https://git.kernel.org/pub/scm/utils/dash/dash.git"
    url      = "https://git.kernel.org/pub/scm/utils/dash/dash.git/snapshot/dash-0.5.9.1.tar.gz"
    list_url = homepage

    version('0.5.11.3', sha256='683202b5b9ff704d963ea0c80345c0fade23233d0b7570e687cc7f652e8bc850')
    version('0.5.11.2', sha256='24b0bfea976df722bc360e782b683c0867f0513d2922fa3c002d8d47a20605ee')
    version('0.5.11.1', sha256='9bc46dc83ecabb975ceb9d8ba2f40c7a25dd1d0825a2cd74b4dc4a62cf2b0c18')
    version('0.5.11',   sha256='8bc06c1314e5197f35b6e158bb74d609d993b0887a4f26e3be0d9182381f3443')
    version('0.5.10.2', sha256='c34e1259c4179a6551dc3ceb41c668cf3be0135c5ec430deb2edfc17fff44da9')
    version('0.5.10.1', sha256='6e8867b586ba23a2ed7e705cef107665acf30153e9c68946fb27084a7edff29b')
    version('0.5.10',   sha256='4267f25a164836b467ba9597a749141a37f18a9dc8dc0b270f8a6f12bab0debc')
    version('0.5.9.1', sha256='3f747013a20a3a9d2932be1a6dd1b002ca5649849b649be0af8a8da80bd8a918')

    depends_on('libedit', type='link')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def configure_args(self):
        # Compile with libedit support
        # This allows the use of arrow keys at the command line
        # See https://askubuntu.com/questions/704688
        return ['--with-libedit']
