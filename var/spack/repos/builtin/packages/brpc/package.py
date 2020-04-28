# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Brpc(CMakePackage):
    """An industrial-grade RPC framework used throughout Baidu, with
    1,000,000+ instances(not counting clients) and thousands kinds of
    services, called "baidu-rpc" inside Baidu. Only C++ implementatioo
    on is opensourced right now."""

    homepage = "https://github.com/apache/incubator-brpc"
    url      = "https://github.com/apache/incubator-brpc/archive/0.9.7-rc03.tar.gz"

    version('0.9.7-rc03', sha256='baacaed6c1dcdda06cb686fc4a5218da3649b9727436288d0369a68d475e1d93')
    version('0.9.7-rc02', sha256='ad43e5d728d8195f9e761910eaf0a6074ad32073d035b9d3ff3b8571cdb89563')
    version('0.9.7-rc01', sha256='bf68452bd66b92dcb65a9378fe340a8e5a5b3008094ba951da3d65ad906e2aa0')

    depends_on('gflags')
    depends_on('protobuf')
    depends_on('leveldb')

    patch('narrow.patch',
        sha256='d7393029443853ddda6c09e3d2185ac2f60920a36a8b685eb83b6b80c1535539')
