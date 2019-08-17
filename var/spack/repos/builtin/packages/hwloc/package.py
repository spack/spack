# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
    url      = "https://download.open-mpi.org/release/hwloc/v2.0/hwloc-2.0.2.tar.gz"
    list_url = "http://www.open-mpi.org/software/hwloc/"
    list_depth = 2

    version('2.0.2',  '71d1211eaa4b25ac7ad80cf326784e87')
    version('2.0.1',  '442b2482bb5b81983ed256522aadbf94')
    version('2.0.0',  '027e6928ae0b5b64c821d0a71a61cd82')
    version('1.11.11', sha256='74329da3be1b25de8e98a712adb28b14e561889244bf3a8138afe91ab18e0b3a')
    version('1.11.10', sha256='0a2530b739d9ebf60c4c1e86adb5451a20d9e78f7798cf78d0147cc6df328aac')
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

    variant('nvml', default=False, description="Support NVML device discovery")
    variant('gl', default=False, description="Support GL device discovery")
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

    depends_on('cuda', when='+nvml')
    depends_on('cuda', when='+cuda')
    depends_on('gl', when='+gl')
    depends_on('libpciaccess', when='+pci')
    depends_on('libxml2', when='+libxml2')
    depends_on('cairo', when='+cairo')
    depends_on('numactl', when='@:1.11.11 platform=linux')

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
        args.extend(self.enable_or_disable('nvml'))
        args.extend(self.enable_or_disable('gl'))
        args.extend(self.enable_or_disable('cuda'))
        args.extend(self.enable_or_disable('libxml2'))
        args.extend(self.enable_or_disable('pci'))
        args.extend(self.enable_or_disable('shared'))

        return args
