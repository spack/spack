##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import re
from six.moves.urllib.parse import urlparse


class Aspell(AutotoolsPackage):
    """GNU Aspell is a Free and Open Source spell checker designed to 
    eventually replace Ispell."""

    homepage = "http://aspell.net/"
    url      = "https://ftpmirror.gnu.org/aspell/aspell-0.60.6.1.tar.gz"

    version('0.60.6.1', 'e66a9c9af6a60dc46134fdacf6ce97d7')

    # additional dictionaries here: ftp://ftp.gnu.org/gnu/aspell/dict/0index.html
    dicts = [
        {'url': 'ftp://ftp.gnu.org/gnu/aspell/dict/en/aspell6-en-2017.01.22-0.tar.bz2',
         'md5': "a6e002076574de9dc4915967032a1dab",
        },
        {'url': 'ftp://ftp.gnu.org/gnu/aspell/dict/es/aspell6-es-1.11-2.tar.bz2',
         'md5': '8406336a89c64e47e96f4153d0af70c4',
        },
        {'url': 'ftp://ftp.gnu.org/gnu/aspell/dict/de/aspell6-de-20030222-1.tar.bz2',
         'md5': '5950c5c8a36fc93d4d7616591bace6a6',
        },
    ]
    for d in dicts:
        o = urlparse(d['url'])
        p = o.path.split('/')
        d['name'] = p[4]
        d['package'] = re.sub(r'\.tar.gz', '', p[5])

        variant(d['name'], default=False, description=d['package'])
        resource(
            name=d['name'],
            url=d['url'],
            md5=d['md5'],
            placement=d['package'],
            when='+{0}'.format(d['name']),
        )

    # When installing dictionaries, prezip needs to be able to find
    # prezip-bin.
    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('PATH', self.prefix.bin)

    @run_after('install')
    def install_dictionaries(self):
        prefix = self.prefix
        for d in self.dicts:
            if '+{0}'.format(d['name']) in self.spec:
                with working_dir(d['package']):
                    bash = which('bash')
                    make = which('make')
                    aspell = join_path(prefix.bin, "aspell")
                    prezip = join_path(prefix.bin, "prezip")
                    bash('./configure', '--vars', "ASPELL={0}".format(aspell),
                         "PREZIP={0}".format(prezip))
                    make('install')
