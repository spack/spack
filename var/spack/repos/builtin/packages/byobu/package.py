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
#
from spack import *


class Byobu(AutotoolsPackage):
    """Byobu is a GPLv3 open source text-based window manager and terminal
multiplexer.  It was originally designed to provide elegant enhancements to the
otherwise functional, plain, practical GNU Screen, for the Ubuntu server
distribution. Byobu now includes an enhanced profiles, convenient keybindings,
configuration utilities, and toggle-able system status notifications for both
the GNU Screen window manager and the more modern Tmux terminal multiplexer,
and works on most Linux, BSD, and Mac distributions.
    """

    homepage = "http://byobu.co"
    url	     = "https://launchpad.net/byobu/trunk/5.123/+download/byobu_5.123.orig.tar.gz"

    version('5.123', '961e0072c01c78c9ce4c20d1aa1b0dc4')

    depends_on('tmux')

