# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cassandra(Package):
    """
    Apache Cassandra is a highly-scalable partitioned row store. Rows are
    organized into tables with a required primary key.
    """

    homepage = "https://github.com/apache/cassandra"
    url      = "https://archive.apache.org/dist/cassandra/4.0.1/apache-cassandra-4.0.1-bin.tar.gz"

    version('4.0.1',   sha256='ed7022e30d9b77d9ce1072f8de95ab01ef7c5c6ed30f304e413dd5a3f92a52f8')
    version('4.0.0',   sha256='2ff17bda7126c50a2d4b26fe6169807f35d2db9e308dc2851109e1c7438ac2f1')
    version('3.11.11', sha256='a5639af781005410995a96f512d505c1def7b70cf5bbbec52e7cd5ff31b6cea3')
    version('3.10',    sha256='c09c3f92d4f80d5639e3f1624c9eec45d25793bbb6b3e3640937b68a9c6d107f')
    version('3.9',     sha256='27cf88a6bce1ee2fb1a1c936094b9200ad844414c2b5b1491ba4991fcc0fd693')
    version('3.8',     sha256='cfae17f040c836dbe37e1d14737c804f60995d30e3a9d03ab6f42d373f0e2efc')
    version('3.7',     sha256='335f5344c4e6b98ec51324d821fa06e99101145ac6e83b5f6ede8c0ca5d15748')
    version('3.6',     sha256='a568f80e224c497a7fb0edaad760960c79fef772d8c66ebf3960434982e8d079')
    version('3.5',     sha256='b575990dfa53567bc67407318330f9406750f4543a9d385b0fce326eb430bf4f')
    version('3.4',     sha256='6fea829d5c9e3c34448d519fb9744e645de921d12702cf2bc10b36f17d738794')
    version('3.3',     sha256='d98e685857d80f9eb93529f7b4f0f2c369ef40974866c8f8ad8edd3d6e0bf7e3')
    version('3.2',     sha256='80ccb14e08313c4c87b6c7d703676a20d948116544f2a0d2eb1c93a22d1be423')
    version('3.1',     sha256='c09c3f92d4f80d5639e3f1624c9eec45d25793bbb6b3e3640937b68a9c6d107f')
    version('3.0.25',  sha256='088bffef5a996e7d7774e698e6b30f7bf9ee86ba2656c829464e0a8bb9fcb75d')
    version('2.2.19',  sha256='5496c0254a66b6d50bde7999d1bab9129b0406b71ad3318558f4d7dbfbed0ab9')
    version('2.1.22',  sha256='e37b46196d9cd9fec8383f94336656037e9a8ce8b3a1867c6986d5097e3b65f2')
    version('2.0.17',  sha256='ba56e3176c385a4be16f48bf8bbbf6ffee10774dcf909c19fd77783ac402071c')
    version('1.2.19',  sha256='1c0c6e62dc612a43d6cb54bc70054876576a6cae7b90aca2162aa379df1b787e')
    version('1.1.12',  sha256='3600f6e86e76974b38b2bf90fabff99ab2a443f444d55a93f3c677c8edbe3785')
    version('1.0.12',  sha256='97f2896263960aa53faa201b07d5a89d531d5e2ab3d9d788e5fc5bc5e9ef985a')

    depends_on('java@9:', type=('build', 'run'), when='@4.0.0:')
    depends_on('java@:8', type=('build', 'run'), when='@:3.11.11')

    def install(self, spec, prefix):
        install_tree('.', prefix)
