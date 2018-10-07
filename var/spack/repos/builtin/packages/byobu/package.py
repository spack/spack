# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Byobu(AutotoolsPackage):
    """Byobu: Text-based window manager and terminal multiplexer."""

    homepage = "http://www.byobu.co"
    url      = "https://launchpad.net/byobu/trunk/5.123/+download/byobu_5.123.orig.tar.gz"

    version('5.125', 'f90f15771325e8be9360f301b52182d2')
    version('5.123', '961e0072c01c78c9ce4c20d1aa1b0dc4')

    depends_on('tmux', type=('build', 'run'))
