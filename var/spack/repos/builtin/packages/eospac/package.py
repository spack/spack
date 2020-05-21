# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Eospac(Package):
    """A collection of C routines that can be used to access the Sesame data
       library.
    """

    homepage = "http://laws.lanl.gov/projects/data/eos.html"
    list_url = "http://laws.lanl.gov/projects/data/eos/eospacReleases.php"

    version('6.4.0',       sha256='15a953beac735c68431afe86ffe33323d540d0fbbbec03ba79438dd29736051d', preferred=True,
            url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0_612ea8c9b8ffa6d9175d9118955571d9107f1e3c.tgz")
    version('6.4.0beta.4', sha256='0ebfd8badff575ea77444aa978629dbdca3135a0b5eb373b8daba058773d4635',
            url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.4_aff6429bb6868de31a980278bafa13487c2ce83f.tgz")
    version('6.4.0beta.3', sha256='9f387ca5356519494c6f3f27adb0c165cf9f9e15e3355a67bf940a4a92eebdab',
            url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.3_90ff265f62aa1780bfcd0a62dad807b6be6ed461.tgz")
    version('6.4.0beta.2', sha256='f9db46cd6c62a6f83960d802350f3e37675921af102969b293c02eb797558a53',
            url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.2_69196eadbc77506561eef711f19d2f03b4ab0ffa.tgz")
    version('6.4.0beta.1', sha256='14c5c804e5f628f41e8ed80bcee5a80adeb6c6f3d130715421ca99a30c7eb7e2',
            url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.1_r20171213193219.tgz")
    version('6.3.1',       sha256='aa1112c4251c9c3c2883a7ab2c7f2abff2c339f29dbbf8421ef88b0c9df904f8',
            url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.3.1_r20161202150449.tgz")

    # This patch allows the use of spack's compile wrapper 'flang'
    patch('flang.patch', when='@:6.4.0beta.2%clang')

    def install(self, spec, prefix):
        with working_dir('Source'):
            make('install',
                 'CC={0}'.format(spack_cc),
                 'CXX={0}'.format(spack_cxx),
                 'F77={0}'.format(spack_f77),
                 'F90={0}'.format(spack_fc),
                 'prefix={0}'.format(prefix),
                 'INSTALLED_LIBRARY_DIR={0}'.format(prefix.lib),
                 'INSTALLED_INCLUDE_DIR={0}'.format(prefix.include),
                 'INSTALLED_EXAMPLE_DIR={0}'.format(prefix.example),
                 'INSTALLED_BIN_DIR={0}'.format(prefix.bin))

        # fix conflict with linux's getopt for 6.4.0beta.2
        if spec.satisfies('@6.4.0beta.2'):
            with working_dir(prefix.bin):
                move('getopt', 'driver_getopt')
