# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LxdeCommon(AutotoolsPackage):
    """lxde package  common components"""

    homepage = "http://lxde.org/"
    url      = "https://downloads.sourceforge.net/project/lxde/lxde-common%20%28default%20config%29/lxde-common%200.99/lxde-common-0.99.1.tar.xz"

    version('0.99.1', '3ab92bd7bcff8bc8e6395651d164cf76')

    depends_on('gtkplus')
