# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Clp(AutotoolsPackage):
    """Clp (Coin-or linear programming) is an open-source
      linear programming solver written in C++."""

    homepage = "https://projects.coin-or.org/Clp"
    url      = "https://www.coin-or.org/download/source/Clp/Clp-1.16.11.tgz"

    version('1.16.11', sha256='b525451423a9a09a043e6a13d9436e13e3ee7a7049f558ad41a110742fa65f39')

    build_directory = 'spack-build'

    def configure_args(self):
        args = []
        for d in [join_path('BuildTools', 'config.guess'),
                  join_path('Clp', 'config.guess'),
                  join_path('ThirdParty', 'ASL', 'config.guess'),
                  join_path('ThirdParty', 'Blas', 'config.guess'),
                  join_path('ThirdParty', 'Lapack', 'config.guess'),
                  join_path('ThirdParty', 'Metis', 'config.guess'),
                  join_path('ThirdParty', 'Mumps', 'config.guess'),
                  join_path('ThirdParty', 'Glpk', 'config.guess'),
                  join_path('Data', 'Netlib', 'config.guess'),
                  join_path('Data', 'Sample', 'config.guess'),
                  join_path('CoinUtils', 'config.guess'),
                  join_path('Osi', 'config.guess')]:
            copy('config.guess', d)

        return args
