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


class Tmux(Package):
    """tmux is a terminal multiplexer. What is a terminal multiplexer? It lets
       you switch easily between several programs in one terminal, detach them
       (they keep running in the background) and reattach them to a different
       terminal. And do a lot more.
    """

    homepage = "http://tmux.github.io"
    url = "https://github.com/tmux/tmux/releases/download/2.2/tmux-2.2.tar.gz"

    version('2.3', 'fcfd1611d705d8b31df3c26ebc93bd3e')
    version('2.2', 'bd95ee7205e489c62c616bb7af040099')
    version('2.1', '74a2855695bccb51b6e301383ad4818c')
    version('1.9a', 'b07601711f96f1d260b390513b509a2d')

    depends_on('libevent')
    depends_on('ncurses')

    def install(self, spec, prefix):
        pkg_config_path = ':'.join([
            spec['libevent'].prefix,
            spec['ncurses'].prefix
        ])

        configure(
            "--prefix=%s" % prefix,
            "PKG_CONFIG_PATH=%s" % pkg_config_path)

        make()
        make("install")
