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


class Libpcap(AutotoolsPackage):
    """The Packet Capture library provides a high level interface to packet
    capture systems. All packets on the network, even those destined for
    other hosts, are accessible through this mechanism. It also supports
    saving captured packets to a ``savefile'', and reading packets from
    a ``savefile''.

    WARNING: In order for libpcap to be able to capture packets on a Linux
    system, the "packet" protocol must be supported by your kernel.  If it
    is not, you may get error messages such as

    ``modprobe: can't locate module net-pf-17``

    in "/var/adm/messages", or may get messages such as

    ``socket: Address family not supported by protocol``

    from applications using libpcap.

    The above was taken from README.linux from the main repository homepage,
    refer to the README for your operating system for more information.
    """

    homepage = "http://www.tcpdump.org/"
    url      = "http://www.tcpdump.org/release/libpcap-1.8.1.tar.gz"

    version('1.8.1',    '3d48f9cd171ff12b0efd9134b52f1447')

    variant("libnl", default=True,
            description="libpcap states a strong preference to using libnl.")

    # Unsure of deps, link flag for libnl3, hard version 3.2.25 only because
    # it is the first version packaged.
    depends_on("libnl@3.2.25:", when="+libnl", type=("build", "link", "run"))

    depends_on("flex",  type="build")
    depends_on("m4",    type="build")
    depends_on("bison", type="build")
    depends_on("pkg-config", type="build")

    def configure_args(self):
        args = []
        spec = self.spec
        if "+libnl" in spec:
            args.extend([
                'CFLAGS=-I{0}'.format(spec["libnl"].prefix.include),
                'LDFLAGS=-L{0}'.format(spec["libnl"].prefix.lib),
                'LIBS=-lnl-3'
            ])
        else:
            args.append("--without-libnl")

        return args
