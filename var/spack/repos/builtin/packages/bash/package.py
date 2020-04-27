# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bash(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Project's Bourne Again SHell."""

    homepage = "https://www.gnu.org/software/bash/"
    gnu_mirror_path = "bash/bash-4.4.tar.gz"

    version('5.0',    sha256='b4a80f2ac66170b2913efbfb9f2594f1f76c7b1afd11f799e22035d63077fb4d')
    version('4.4.12', sha256='57d8432be54541531a496fd4904fdc08c12542f43605a9202594fa5d5f9f2331')
    version('4.4',    sha256='d86b3392c1202e8ff5a423b302e6284db7f8f435ea9f39b5b1b20fd3ac36dfcb')
    version('4.3',    sha256='afc687a28e0e24dc21b988fa159ff9dbcf6b7caa92ade8645cc6d5605cd024d4')

    depends_on('ncurses')
    depends_on('readline@5.0:')
    depends_on('iconv')

    patches = [
        ('5.0', '001', 'f2fe9e1f0faddf14ab9bfa88d450a75e5d028fedafad23b88716bd657c737289'),
        ('5.0', '002', '87e87d3542e598799adb3e7e01c8165bc743e136a400ed0de015845f7ff68707'),
        ('5.0', '003', '4eebcdc37b13793a232c5f2f498a5fcbf7da0ecb3da2059391c096db620ec85b'),
        ('5.0', '004', '14447ad832add8ecfafdce5384badd933697b559c4688d6b9e3d36ff36c62f08'),
        ('5.0', '005', '5bf54dd9bd2c211d2bfb34a49e2c741f2ed5e338767e9ce9f4d41254bf9f8276'),
        ('5.0', '006', 'd68529a6ff201b6ff5915318ab12fc16b8a0ebb77fda3308303fcc1e13398420'),
        ('5.0', '007', '17b41e7ee3673d8887dd25992417a398677533ab8827938aa41fad70df19af9b'),
        ('5.0', '008', 'eec64588622a82a5029b2776e218a75a3640bef4953f09d6ee1f4199670ad7e3'),
        ('5.0', '009', 'ed3ca21767303fc3de93934aa524c2e920787c506b601cc40a4897d4b094d903'),
        ('5.0', '010', 'd6fbc325f0b5dc54ddbe8ee43020bced8bd589ddffea59d128db14b2e52a8a11'),
        ('5.0', '011', '2c4de332b91eaf797abbbd6c79709690b5cbd48b12e8dfe748096dbd7bf474ea'),
        ('5.0', '012', '2943ee19688018296f2a04dbfe30b7138b889700efa8ff1c0524af271e0ee233'),
        ('5.0', '013', 'f5d7178d8da30799e01b83a0802018d913d6aa972dd2ddad3b927f3f3eb7099a'),
        ('5.0', '014', '5d6eee6514ee6e22a87bba8d22be0a8621a0ae119246f1c5a9a35db1f72af589'),
        ('5.0', '015', 'a517df2dda93b26d5cbf00effefea93e3a4ccd6652f152f4109170544ebfa05e'),
        ('5.0', '016', 'ffd1d7a54a99fa7f5b1825e4f7e95d8c8876bc2ca151f150e751d429c650b06d'),
    ]

    # TODO: patches below are not managed by the GNUMirrorPackage base class
    for ver, num, checksum in patches:
        ver = Version(ver)
        patch('https://ftpmirror.gnu.org/bash/bash-{0}-patches/bash{1}-{2}'.format(ver, ver.joined, num),
              level=0, when='@{0}'.format(ver), sha256=checksum)

    def configure_args(self):
        spec = self.spec

        return [
            'LIBS=-lncursesw',
            '--with-curses',
            '--enable-readline',
            '--with-installed-readline',
            '--with-libiconv-prefix={0}'.format(spec['iconv'].prefix),
        ]

    def check(self):
        make('tests')

    @property
    def install_targets(self):
        args = ['install']

        if self.spec.satisfies('@4.4:'):
            args.append('install-headers')

        return args
