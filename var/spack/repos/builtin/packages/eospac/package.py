# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Eospac(Package):
    """A collection of C routines that can be used to access the Sesame data
       library.
    """

    homepage = "https://laws.lanl.gov/projects/data/eos.html"
    list_url = "https://laws.lanl.gov/projects/data/eos/eospacReleases.php"

    version('6.4.0', 'ecee3abe9c7a3e4b32d68dc3177b088e',
            url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0_612ea8c9b8ffa6d9175d9118955571d9107f1e3c.tgz")
    version('6.4.0beta.4', 'd0875390d08538a3caa8ad1f43c6d789',
            url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.4_aff6429bb6868de31a980278bafa13487c2ce83f.tgz")
    version('6.4.0beta.3', '672c16e522908281168815a74626ec66',
            url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.3_90ff265f62aa1780bfcd0a62dad807b6be6ed461.tgz")
    version('6.4.0beta.2', '9b6e48090647221d5ffe7ec5f9ea4c71',
            url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.2_69196eadbc77506561eef711f19d2f03b4ab0ffa.tgz")
    version('6.4.0beta.1', 'e4e4beabf946f0b8953532832002afc2',
            url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.1_r20171213193219.tgz")
    version('6.3.1', '549fda008c4169a69b02ec2a9de1e434', preferred=True,
            url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.3.1_r20161202150449.tgz")

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
