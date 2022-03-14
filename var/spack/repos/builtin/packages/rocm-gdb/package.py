# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmGdb(AutotoolsPackage):
    """This is ROCmgdb, the ROCm source-level debugger for Linux,
        based on GDB, the GNU source-level debugger."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCgdb/"
    url      = "https://github.com/ROCm-Developer-Tools/ROCgdb/archive/rocm-4.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']
    version('4.5.2', sha256='e278abf50f1758ce396b26a6719d0af09a6053c195516a44ec9b2be925d79203')
    version('4.5.0', sha256='dd37c8b1ea6bb41b1263183637575d7bf4746cabc573dbff888e23b0379877b0')
    version('4.3.1', sha256='995756a24b1e1510647dac1476a3a9a8e3af8e9fd9f4af1d00dd2db28e7a4ef2')
    version('4.3.0', sha256='8ee0667ab2cd91b2cc41d3a7af046d36a6b4e2007f050265aa65e0aedec83fd7')
    version('4.2.0', sha256='4bc579584a1f8614111e7e44d8aa1c6d5d06be3f5db055aba2cf1abc140122ac')
    version('4.1.0', sha256='28dc806e48695d654d52fb1a634df6d4c1243f00846ae90161e7a5e9f4d88b24', deprecated=True)
    version('4.0.0', sha256='b90291b0a8409fe66d8a65d2731dcb87b9f5a22bac9ce3ffbab726eb129ba13d', deprecated=True)
    version('3.10.0', sha256='05455cb47dd42404ee8bba047def6a6846a7e877e7a7db8dcffc7100d5ba16f0', deprecated=True)
    version('3.9.0', sha256='0765c96439c0efa145418d210d865b9faed463466d7522274959cc4476a37097', deprecated=True)
    version('3.8.0', sha256='a7c11dc30c952587c616bf7769bad603c3bf80522afc8b73ccda5b78d27bed41', deprecated=True)
    version('3.7.0', sha256='7a29ef584fd7b6c66bb03aaf8ec2f5a8c758370672a28a4d0d95066e5f6fbdc1', deprecated=True)
    version('3.5.0', sha256='cf36d956e84c7a5711b71f281a44b0a9708e13e941d8fca0247d01567e7ee7d1', deprecated=True)

    depends_on('cmake@3:', type='build')
    depends_on('texinfo', type='build')
    depends_on('bison', type='build')
    depends_on('flex@2.6.4:', type='build')
    depends_on('libunwind', type='build')
    depends_on('expat', type=('build', 'link'))
    depends_on('python', type=('build', 'link'))
    depends_on('zlib', type='link')
    depends_on('babeltrace@1.2.4', type='link')
    depends_on('gmp',      type=('build', 'link'), when='@4.5.0:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2']:
        depends_on('rocm-dbgapi@' + ver, type='link', when='@' + ver)
        depends_on('comgr@' + ver, type='link', when='@' + ver)

    build_directory = 'spack-build'

    def configure_args(self):
        # Generic options to compile GCC
        options = [
            # Distributor options
            '--program-prefix=roc',
            '--enable-64-bit-bfd',
            '--with-bugurl=https://github.com/ROCm-Developer-Tools/ROCgdb/issues',
            '--with-pkgversion=-ROCm',
            '--enable-targets=x86_64-linux-gnu,amdgcn-amd-amdhsa',
            '--disable-ld',
            '--disable-gas',
            '--disable-gdbserver',
            '--disable-sim',
            '--enable-tui',
            '--disable-gdbtk',
            '--disable-shared',
            '--with-expat',
            '--with-system-zlib'
            '--without-guile',
            '--with-babeltrace',
            '--with-lzma',
            '--with-python',
            '--with-rocm-dbgapi={0}'.format(self.spec['rocm-dbgapi'].prefix)
        ]
        return options
