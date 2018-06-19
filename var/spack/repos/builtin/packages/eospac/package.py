##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Eospac(Package):
    """A collection of C routines that can be used to access the Sesame data
       library.
    """

    homepage = "https://laws.lanl.gov/projects/data/eos.html"
    list_url = "https://laws.lanl.gov/projects/data/eos/eospacReleases.php"

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
