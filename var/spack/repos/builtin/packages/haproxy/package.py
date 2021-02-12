# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Haproxy(MakefilePackage):
    """
    HAProxy is a single-threaded, event-driven, non-blocking engine
    combining a very fast I/O layer with a priority-based scheduler.
    """

    homepage = "https://www.haproxy.org"
    url      = "https://www.haproxy.org/download/2.1/src/haproxy-2.1.0.tar.gz"

    version('2.1.11', sha256='feff37a5459d7aca8fcca50fa0e6d20d176394019cec3be17ec9c6ba0fdbdbad')
    version('2.1.10', sha256='d245a06145d1d0cbe62681de84bc23dfc98afe10f8cc5c1422a447722a142a41')
    version('2.1.9',  sha256='ed26c652ba9c0fef1207dabb5c1db70962254bb1e8892955b6dc119576904627')
    version('2.1.8',  sha256='7ad288fdf55c45cb7a429b646afb0239311386a9746682787ae430b70ab1296a')
    version('2.1.7',  sha256='392e6cf18e75fe7e166102e8c4512942890a0b5ae738f6064faab4687f60a339')
    version('2.1.6',  sha256='e65d9be9c01cb018200ed602c6d12d5a5cfe54e2318675b74009d936d923dfdf')
    version('2.1.5',  sha256='42174ac5836ab243565b888299ec30115c1259e75872696708528260c6700ea1')
    version('2.1.4',  sha256='51030ff696d7067162b4d24d354044293aecfbb36d7acc2f840c8d928bfe91cd')
    version('2.1.3',  sha256='bb678e550374d0d9d9312885fb9d270b501dae9e3b336f0a4379c667dae00b59')
    version('2.1.2',  sha256='6079b08a8905ade5a9a2835ead8963ee10a855d8508a85efb7181eea2d310b77')
    version('2.1.1', sha256='57e75c1a380fc6f6aa7033f71384370899443c7f4e8a4ba289b5d4350bc76d1a')
    version('2.1.0', sha256='f268efb360a0e925137b4b8ed431f2f8f3b68327efb2c418b266e535d8e335a0')

    def url_for_version(self, version):
        url = "https://www.haproxy.org/download/{0}/src/haproxy-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def build(self, spec, prefix):
        make('TARGET=generic', 'PREFIX=' + prefix)

    def install(self, spec, prefix):
        install_tree('.', prefix)
