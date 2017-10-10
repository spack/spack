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


class Libnl(AutotoolsPackage):
    """The libnl suite is a collection of libraries providing APIs to netlink
    protocol based Linux kernel interfaces.

    Netlink is a IPC mechanism primarly between the kernel and user space
    processes. It was designed to be a more flexible successor to ioctl to
    provide mainly networking related kernel configuration and monitoring
    interfaces.
    """

    homepage = "https://www.infradead.org/~tgr/libnl/"
    url      = "https://www.infradead.org/~tgr/libnl/files/libnl-3.2.25.tar.gz"

    version('3.2.25', '03f74d0cd5037cadc8cdfa313bbd195c')

    depends_on("flex",  type="build")
    depends_on("m4",    type="build")
    depends_on("bison", type="build")

    # NOTE: there is something in the configure about pthreads, but
    #       I do not understand the `spack` + `pthreads` relationship.
