##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
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


class Cquery(WafPackage):
    """C/C++ language server supporting multi-million line code base, powered
    by libclang."""

    homepage = "https://github.com/cquery-project/cquery"
    url      = "https://github.com/cquery-project/cquery/archive/v20180302.tar.gz"
    base_url = 'https://github.com/cquery-project/cquery/archive/v{0}.tar.gz'

    releases = [
        {
            'version': '20180302',
            'md5': '23eabb9640cfb4de614873314aafb427',
            'resources': {
                'doctest': 'b40b7e799deabac916d631d181a7f19f3060acc5',
                'loguru': '2c35b5e7251ab5d364b1b3164eccef7b5d2293c5',
                'msgpack-c': '208595b2620cf6260ce3d6d4cf8543f13b206449',
                'rapidjson': 'daabb88e001f562e1f7df5f44d7fed32a0c107c2',
                'sparsepp': '1ca7189fe81ee8c59bf08196852f70843a68a63a'
            }
        },
    ]

    resources = {
        'doctest': {
            'url': 'https://github.com/onqtam/doctest.git',
        },
        'loguru': {
            'url': 'https://github.com/emilk/loguru.git',
        },
        'msgpack-c': {
            'url': 'https://github.com/msgpack/msgpack-c.git',
        },
        'rapidjson': {
            'url': 'https://github.com/miloyip/rapidjson.git',
        },
        'sparsepp': {
            'url': 'https://github.com/greg7mdp/sparsepp.git',
        },
    }

    for release in releases:
        version(release['version'], release['md5'],
                url=base_url.format(release['version']))

        for name, commit in release['resources'].items():
            resource(name=name,
                     git=resources[name]['url'],
                     commit=commit,
                     placement='{0}'.format(name),
                     destination='third_party'
                     )

    depends_on('llvm@3.3:+clang')

    def configure_args(self):
        return ['--llvm-config=llvm-config']


    # FIXME: Override configure_args(), build_args(),
    # or install_args() if necessary.
