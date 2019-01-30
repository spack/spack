# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Appres(AutotoolsPackage):
    """The appres program prints the resources seen by an application (or
    subhierarchy of an application) with the specified class and instance
    names.  It can be used to determine which resources a particular
    program will load."""

    homepage = "http://cgit.freedesktop.org/xorg/app/appres"
    url      = "https://www.x.org/archive/individual/app/appres-1.0.4.tar.gz"

    version('1.0.4', 'f82aabe6bbb8960781b63c6945bb361b')

    depends_on('libx11')
    depends_on('libxt')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
