# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hbase(Package):
    """
    Apache HBase is an open-source, distributed, versioned, column-oriented
    store modeled after Google' Bigtable: A Distributed Storage System for
    Structured Data by Chang et al. Just as Bigtable leverages the distributed
    data storage provided by the Google File System, HBase provides
    Bigtable-like capabilities on top of Apache Hadoop.
    """

    homepage = "https://github.com/apache/hbase"
    url      = "https://github.com/apache/hbase/archive/rel/2.2.2.tar.gz"

    version('2.2.2',    sha256='e9a58946e9adff1cac23a0b261ecf32da32f8d2ced0706af1d04e8a67d582926')
    version('2.1.8',    sha256='121cea4c554879c8401f676c8eb49e39bd35d41c358e919379ad4a318844c8de')

    depends_on('java@7:', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
