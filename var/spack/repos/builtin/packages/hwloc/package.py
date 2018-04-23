##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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

from spack import *
import sys


class Hwloc(AutotoolsPackage):
    """The Hardware Locality (hwloc) software project.

    The Portable Hardware Locality (hwloc) software package
    provides a portable abstraction (across OS, versions,
    architectures, ...) of the hierarchical topology of modern
    architectures, including NUMA memory nodes, sockets, shared
    caches, cores and simultaneous multithreading. It also gathers
    various system attributes such as cache and memory information
    as well as the locality of I/O devices such as network
    interfaces, InfiniBand HCAs or GPUs. It primarily aims at
    helping applications with gathering information about modern
    computing hardware so as to exploit it accordingly and
    efficiently.
    """

    homepage = "http://www.open-mpi.org/projects/hwloc/"
    url      = "http://www.open-mpi.org/software/hwloc/v1.9/downloads/hwloc-1.9.tar.gz"
    list_url = "http://www.open-mpi.org/software/hwloc/"
    list_depth = 2

    version('2.0.1',  '442b2482bb5b81983ed256522aadbf94')
    version('2.0.0',  '027e6928ae0b5b64c821d0a71a61cd82')
    version('1.11.9', '4d5f5da8b1d09731d82e865ecf3fa399')
    version('1.11.8', 'a0fa1c9109a4d8b4b6568e62cc9b6e30')
    version('1.11.7', '867a5266675e5bf1ef4ab66c459653f8')
    version('1.11.6', 'b4e95eadd2fbdb6d40bbd96be6f03c84')
    version('1.11.5', '8f5fe6a9be2eb478409ad5e640b2d3ba')
    version('1.11.4', 'b6f23eb59074fd09fdd84905d50b103d')
    version('1.11.3', 'c1d36a9de6028eac1d18ea4782ef958f')
    version('1.11.2', 'e4ca55c2a5c5656da4a4e37c8fc51b23')
    version('1.11.1', 'feb4e416a1b25963ed565d8b42252fdc')
    version('1.9',    '1f9f9155682fe8946a97c08896109508')

    variant('cuda', default=False, description="Support CUDA devices")
    variant('libxml2', default=True, description="Build with libxml2")
    variant('pci', default=(sys.platform != 'darwin'),
            description="Support analyzing devices on PCI bus")
    variant('shared', default=True, description="Build shared libraries")
    variant(
        'cairo',
        default=False,
        description='Enable the Cairo back-end of hwloc\'s lstopo command'
    )

    depends_on('pkgconfig', type='build')

    depends_on('cuda', when='+cuda')
    depends_on('libpciaccess', when='+pci')
    depends_on('libxml2', when='+libxml2')
    depends_on('cairo', when='+cairo')
    depends_on('numactl', when='@:1.11.9 platform=linux')

    def url_for_version(self, version):
        return "http://www.open-mpi.org/software/hwloc/v%s/downloads/hwloc-%s.tar.gz" % (version.up_to(2), version)

    def configure_args(self):
        args = [
            # Disable OpenCL, since hwloc might pick up an OpenCL
            # library at build time that is then not found at run time
            # (Alternatively, we could require OpenCL as dependency.)
            "--disable-opencl",
        ]
        if '@2.0.0:' in self.spec:
            args.append('--enable-netloc')

        args.extend(self.enable_or_disable('cairo'))
        args.extend(self.enable_or_disable('cuda'))
        args.extend(self.enable_or_disable('libxml2'))
        args.extend(self.enable_or_disable('pci'))
        args.extend(self.enable_or_disable('shared'))

        return args
