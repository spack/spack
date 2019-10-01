# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tmux(AutotoolsPackage):
    """Tmux is a terminal multiplexer.

    What is a terminal multiplexer? It lets you switch easily between several
    programs in one terminal, detach them (they keep running in the
    background) and reattach them to a different terminal. And do a lot more.
    """

    homepage = "http://tmux.github.io"
    url = "https://github.com/tmux/tmux/releases/download/2.6/tmux-2.6.tar.gz"

    version('2.8', sha256='7f6bf335634fafecff878d78de389562ea7f73a7367f268b66d37ea13617a2ba')
    version('2.7', 'bcdfcf910c94c3e02ce6b1c035880306')
    version('2.6', 'd541ff392249f94c4f3635793556f827')
    version('2.5', '4a5d73d96d8f11b0bdf9b6f15ab76d15')
    version('2.4', '6165d3aca811a3225ef8afbd1afcf1c5')
    version('2.3', 'fcfd1611d705d8b31df3c26ebc93bd3e')
    version('2.2', 'bd95ee7205e489c62c616bb7af040099')
    version('2.1', '74a2855695bccb51b6e301383ad4818c')
    version('1.9a', 'b07601711f96f1d260b390513b509a2d')

    depends_on('libevent')
    depends_on('ncurses')

    def flag_handler(self, name, flags):
        if name == 'cppflags':
            flags.append(self.spec['ncurses'].headers.include_flags)
        return (None, flags, None)

    def configure_args(self):
        return ['LIBTINFO_LIBS=-lncurses']
