# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gdb(AutotoolsPackage):
    """GDB, the GNU Project debugger, allows you to see what is going on
    'inside' another program while it executes -- or what another
    program was doing at the moment it crashed.
    """

    homepage = "https://www.gnu.org/software/gdb"
    url      = "https://ftpmirror.gnu.org/gdb/gdb-7.10.tar.gz"

    version('8.3', sha256='b2266ec592440d0eec18ee1790f8558b3b8a2845b76cc83a872e39b501ce8a28')
    version('8.2.1', sha256='0107985f1edb8dddef6cdd68a4f4e419f5fec0f488cc204f0b7d482c0c6c9282')
    version('8.2', '0783c6d86775c5aff06cccc8a3d7cad8')
    version('8.1', '0c85ecbb43569ec43b1c9230622e84ab')
    version('8.0.1', 'bb45869f8126a84ea2ba13a8c0e7c90e')
    version('8.0', '9bb49d134916e73b2c01d01bf20363df')
    version('7.12.1', '06c8f40521ed65fe36ebc2be29b56942')
    version('7.11', 'f585059252836a981ea5db9a5f8ce97f')
    version('7.10.1', 'b93a2721393e5fa226375b42d567d90b')
    version('7.10', 'fa6827ad0fd2be1daa418abb11a54d86')
    version('7.9.1', 'f3b97de919a9dba84490b2e076ec4cb0')
    version('7.9', '8f8ced422fe462a00e0135a643544f17')
    version('7.8.2', '8b0ea8b3559d3d90b3ff4952f0aeafbc')

    variant('python', default=True, description='Compile with Python support')
    variant('xz', default=True, description='Compile with lzma support')

    # Required dependency
    depends_on('texinfo', type='build')

    # Optional dependencies
    depends_on('python', when='+python')
    depends_on('xz', when='+xz')

    def configure_args(self):
        args = []
        if '+python' in self.spec:
            args.append('--with-python')
            args.append('LDFLAGS={0}'.format(
                self.spec['python'].libs.ld_flags))
        return args
