# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hbase(Package):
    """Apache HBase is an open-source, distributed, versioned, column-oriented
    store modeled after Google' Bigtable: A Distributed Storage System for
    Structured Data by Chang et al. Just as Bigtable leverages the distributed
    data storage provided by the Google File System, HBase provides
    Bigtable-like capabilities on top of Apache Hadoop."""

    homepage = "https://archive.apache.org/"
    url      = "https://archive.apache.org/dist/hbase/2.2.4/hbase-2.2.4-bin.tar.gz"
    list_url = "https://archive.apache.org/dist/hbase"
    list_depth = 1

    version('2.4.1', sha256='2ef95d4b8c8a6a955b25a578b6b336b996233f09abf285fd62cedd8d07a67fc2')
    version('2.4.0', sha256='f1cd67701259a7fc674ae37c92c00ab0dd48be5135164558d70415f9dc7351d1')
    version('2.3.4', sha256='8e1cd63f0be9ab333f9cca08781e614409487cc0ac4ba6b28a29b7ba3edf0827')
    version('2.3.3', sha256='783fec0f1ca67cef53524a2e05f1744c84821454d1a69355e373acb09efeea06')
    version('2.3.2', sha256='ace24523e2c1d732184802f6f6fa9d6dcde1a647a6f89fbdec8484322af94a51')
    version('2.3.1', sha256='f082da6ba9b0fb8270d6a20ead96334590eba62bbfa960f8e74b312d7bc4c00f')
    version('2.3.0', sha256='6b5eb10e7bb624251575551183694ea13de7b57814e440a17e91ecf1784e0951')
    version('2.2.6', sha256='9b7dff72a55cb93acc6005758557d7eb398fd7a41dc27aa07ff41793550a8705')
    version('2.2.5',  sha256='25d08f8f038d9de5beb43dfb0392e8a8b34eae7e0f2670d6c2c172abc3855194')
    version('2.2.4',  sha256='ec91b628352931e22a091a206be93061b6bf5364044a28fb9e82f0023aca3ca4')
    version('2.2.3',  sha256='ea8fa72aa6220e038e30bd7c439d181b10bd7225383f7f2d224ebb5f5397310a')
    version('2.2.2',  sha256='97dcca3a031925a379a0ee6bbfb6007533fb4fdb982c23345e5fc04d6c52bebc')
    version('2.1.8',  sha256='d8296e8405b1c39c73f0dd03fc6b4d2af754035724168fd56e8f2a0ff175ad90')

    depends_on('java@8', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
