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
import sys


class IntelGpuTools(AutotoolsPackage):
    """Intel GPU Tools is a collection of tools for development and testing of
    the Intel DRM driver. There are many macro-level test suites that get used
    against the driver, including xtest, rendercheck, piglit, and oglconform,
    but failures from those can be difficult to track down to kernel changes,
    and many require complicated build procedures or specific testing
    environments to get useful results. Therefore, Intel GPU Tools includes
    low-level tools and tests specifically for development and testing of the
    Intel DRM Driver."""

    homepage = "https://cgit.freedesktop.org/xorg/app/intel-gpu-tools/"
    url      = "https://www.x.org/archive/individual/app/intel-gpu-tools-1.16.tar.gz"

    version('1.16', '3996f10fc86a28ec59e1cf7b227dad78')

    depends_on('libdrm@2.4.64:')
    depends_on('libpciaccess@0.10:', when=(sys.platform != 'darwin'))
    depends_on('cairo@1.12.0:')
    depends_on('glib')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('python@3:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')

    # xrandr ?

    # gtk-doc-tools
    # libunwind-dev
    # python-docutils
    # x11proto-dri2-dev
    # xutils-dev
