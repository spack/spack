# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

from spack import *


class Cutlang(Package):
    """CutLang is a domain specific language that aims to provide a clear,
    human readable way to define analyses in high energy particle physics (HEP)
    along with an interpretation framework of that language."""
    homepage = "https://github.com/unelg/CutLang"
    url      = "https://github.com/unelg/CutLang/archive/refs/tags/v2.12.10.tar.gz"
    maintainers = ['unelg', 'ssekmen', 'sabrivatansever']

    version('2.12.10', sha256='999a2b9fdb4b7d241a6fc21c03d92deadf80ad4682f8ce677ee0fa3b24169bfd', preferred=True)
    version('2.12.9',  sha256='56bfb16f8ed683775fbadbca306cc09bbd65f58f42fa16d98f6d6868e8585b45')
    version('2.12.8',  sha256='d776198fca3c2dcb612cf3bd98f27c069187aa970b80594fdb6681e0643f5e91')
    version('2.12.7',  sha256='f20704abf0f4e04891eb0651f059782eb0f2652661c2c66c70c1bb6d58900380')
    version('2.12.6',  sha256='0fb787457466610d37d1a3f047b68e73ace81e708bd2db76eb84af5a1406377e')
    version('2.12.5',  sha256='eeb31be584551364569bdef8567b4910fd20be4c00bf7dcf07c8c8cbdaa2419c')
    version('2.12.4',  sha256='cc941c358772ada5f66bc768f71bf7841ba2c495dd2bdf132df72a509d5ccb8b')
    version('2.12.3',  sha256='a181fc739d13a7b187a94555b12f0b064e900b1cb69b880c69a9f2877bc5de4c')
    version('2.12.2',  sha256='c2dc8b841bddd58b4e41b104c72c31bb00c750f7fe07672a30c15746dea6734c')
    version('2.12.1',  sha256='7bd7d2e894fdc8465c89970d0011aeaaeae6ec02b4c45d6e2b9111b278ca18a9')
    depends_on('root', type='build')
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    
    def install(self, spec, prefix):
        cmake('..', *std_cmake_args)
        make()
        make('install')
