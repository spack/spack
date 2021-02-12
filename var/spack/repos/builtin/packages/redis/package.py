# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
    url = "http://download.redis.io/releases/redis-5.0.3.tar.gz"

    version('6.0.10', sha256='79bbb894f9dceb33ca699ee3ca4a4e1228be7fb5547aeb2f99d921e86c1285bd')
    version('6.0.9',  sha256='dc2bdcf81c620e9f09cfd12e85d3bc631c897b2db7a55218fd8a65eaa37f86dd')
    version('6.0.8',  sha256='04fa1fddc39bd1aecb6739dd5dd73858a3515b427acd1e2947a66dadce868d68')
    version('6.0.7',  sha256='c2aaa1a4c7e72c70adedf976fdd5e1d34d395989283dab9d7840e0a304bb2393')
    version('6.0.6',  sha256='12ad49b163af5ef39466e8d2f7d212a58172116e5b441eebecb4e6ca22363d94')
    version('6.0.5',  sha256='42cf86a114d2a451b898fcda96acd4d01062a7dbaaad2801d9164a36f898f596')
    version('6.0.4',  sha256='3337005a1e0c3aa293c87c313467ea8ac11984921fab08807998ba765c9943de')
    version('6.0.3',  sha256='bca46dce81fe92f7b2de4cf8ae41fbc4b94fbd5674def7f12c87e7f9165cbb3a')
    version('6.0.2',  sha256='9c37cd4228a57e82e7037094751c63349302b0b86c5e30b778a63a802dfd0109')
    version('6.0.1',  sha256='b8756e430479edc162ba9c44dc89ac394316cd482f2dc6b91bcd5fe12593f273')
    version('6.0.0',  sha256='16d13ec1c3255206deb4818ed444dca6dda1482b551736f0033253c211b788fc')
    version('5.0.10', sha256='e30a5e7d1593a715cdda2a82deb90190816d06c9d1dc1ef5b36874878c683382')
    version('5.0.9',  sha256='53d0ae164cd33536c3d4b720ae9a128ea6166ebf04ff1add3b85f1242090cb85')
    version('5.0.8',  sha256='f3c7eac42f433326a8d981b50dba0169fdfaf46abb23fcda2f933a7552ee4ed7')
    version('5.0.7',  sha256='61db74eabf6801f057fd24b590232f2f337d422280fd19486eca03be87d3a82b')
    version('5.0.6',  sha256='6624841267e142c5d5d5be292d705f8fb6070677687c5aad1645421a936d22b3')
    version('5.0.5',  sha256='2139009799d21d8ff94fc40b7f36ac46699b9e1254086299f8d3b223ca54a375')
    version('5.0.4',  sha256='3ce9ceff5a23f60913e1573f6dfcd4aa53b42d4a2789e28fa53ec2bd28c987dd')
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
