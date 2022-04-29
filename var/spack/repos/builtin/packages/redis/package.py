# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Redis(MakefilePackage):
    """Redis is an open source (BSD licensed), in-memory data structure store,
    used as a database, cache and message broker.
    It supports data structures such as strings, hashes, lists, sets, sorted
    sets with range queries, bitmaps, hyperloglogs, geospatial indexes with
    radius queries and streams. Redis has built-in replication, Lua scripting,
    LRU eviction, transactions and different levels of on-disk persistence,
    and provides high availability via Redis Sentinel and automatic
    partitioning with Redis Cluster
    """
    homepage = "https://redis.io"
    url = "https://download.redis.io/releases/redis-6.2.5.tar.gz"

    version('6.2.5',   sha256='4b9a75709a1b74b3785e20a6c158cab94cf52298aa381eea947a678a60d551ae')
    version('6.2.4',   sha256='ba32c406a10fc2c09426e2be2787d74ff204eb3a2e496d87cff76a476b6ae16e')
    version('6.2.3',   sha256='98ed7d532b5e9671f5df0825bb71f0f37483a16546364049384c63db8764512b')
    version('6.2.2',   sha256='7a260bb74860f1b88c3d5942bf8ba60ca59f121c6dce42d3017bed6add0b9535')
    version('6.2.1',   sha256='cd222505012cce20b25682fca931ec93bd21ae92cb4abfe742cf7b76aa907520')
    version('6.2.0',   sha256='67d624c25d962bd68aff8812a135df85bad07556b8825f3bcd5b522a9932dbca')
    version('6.0.15',  sha256='4bc295264a95bc94423c162a9eee66135a24a51eefe5f53f18fc9bde5c3a9f74')
    version('6.0.5',   sha256='42cf86a114d2a451b898fcda96acd4d01062a7dbaaad2801d9164a36f898f596')
    version('5.0.3',   sha256='e290b4ddf817b26254a74d5d564095b11f9cd20d8f165459efa53eb63cd93e02')
    version('5.0.2',   sha256='937dde6164001c083e87316aa20dad2f8542af089dfcb1cbb64f9c8300cd00ed')
    version('5.0.1',   sha256='82a67c0eec97f9ad379384c30ec391b269e17a3e4596393c808f02db7595abcb')
    version('5.0.0',   sha256='70c98b2d0640b2b73c9d8adb4df63bcb62bad34b788fe46d1634b6cf87dc99a4')
    version('4.0.13',  sha256='17d955227966dcd68590be6139e5fe7f2d19fc4fb7334248a904ea9cdd30c1d4')
    version('4.0.12',  sha256='6447259d2eed426a949c9c13f8fdb2d91fb66d9dc915dd50db13b87f46d93162')
    version('4.0.11',  sha256='fc53e73ae7586bcdacb4b63875d1ff04f68c5474c1ddeda78f00e5ae2eed1bbb')

    @property
    def install_targets(self):
        return [
            'PREFIX={0}'.format(self.spec.prefix),
            'install'
        ]

    @run_after('install')
    def install_conf(self):
        mkdirp(self.prefix.conf)
        install('redis.conf', self.prefix.conf)
