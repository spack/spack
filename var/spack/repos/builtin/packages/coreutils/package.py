# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Coreutils(AutotoolsPackage):
    """The GNU Core Utilities are the basic file, shell and text
       manipulation utilities of the GNU operating system.  These are
       the core utilities which are expected to exist on every
       operating system.
    """
    homepage = "http://www.gnu.org/software/coreutils/"
    url      = "https://ftpmirror.gnu.org/coreutils/coreutils-8.26.tar.xz"

    version('8.29', '960cfe75a42c9907c71439f8eb436303')
    version('8.26', 'd5aa2072f662d4118b9f4c63b94601a6')
    version('8.23', 'abed135279f87ad6762ce57ff6d89c41')

    build_directory = 'spack-build'
