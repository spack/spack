# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lucene(Package):
    """
    Apache Lucene is a high-performance, full featured text search engine
    library written in Java.
    """

    homepage = "https://lucene.apache.org/"
    url      = "http://archive.apache.org/dist/lucene/java/8.3.1/lucene-8.3.1.tgz"
    list_url = "http://archive.apache.org/dist/lucene/java/"
    list_depth = 1

    version('8.8.0', sha256='aaab5a387cefa426a2db20702d97186241b5b989459660f6965750de99b0ed31')
    version('8.7.0', sha256='1b1355b8cb318fb866946d70050e2115e7b6c32bc4da0c3f712237b5e65513ff')
    version('8.6.3', sha256='82d01410dc3e97fabb0840b4e3cf9861ca478d111bd7726fed56ed197f12134d')
    version('8.6.2', sha256='22f49c10c8cd0a4716763e1de7cf77a6e467f28ebd019c590fb637e9aac64b36')
    version('8.6.1', sha256='469b5d2a8dcd1f340371836287282092422f799f3433f7090767b2d69cb14833')
    version('8.6.0', sha256='0f2a17d089da273d16c87c18c6ab02dc13816ed17ffd7cf82b1254888ba42f34')
    version('8.5.2', sha256='70035463f4067afe719b861ad7fdee7cf30ed6cec34de19eb73d425c1487f43f')
    version('8.5.1', sha256='fd1993a157267a2f082e02328561eb9d2fe06729ac7eb151859b77c5e288affd')
    version('8.5.0', sha256='0e0be542847a3bc362837e6de45c15d03089c018aefa2a6608633d65e906ab6a')
    version('8.4.1', sha256='4251cdd9ba23e7b4bbb8c7be788e69d838758d8303cb11452c6dcd2bd2e62a41')
    version('8.4.0', sha256='58b3958c3c5f327c5acdd64be295b74386fe75fcf68c911d427a389827b60be0')
    version('8.3.1', sha256='acd61ad458d16f3c98b9dd4653c6a34dd666a965842e461f7cdf8947fa041e1a')
    version('8.3.0', sha256='67c4f8081f24ff9f4eb4f2b999ac19f7a639b416e5b6f1c1c74e0524a481fc7e')
    version('8.2.0', sha256='505cad34698b217fd6ceee581a8215223a47df5af820c94ca70a6bdbba9d5d7c')
    version('8.1.1', sha256='d62b0acdf2b1ed7a25ccdb593ad8584caeaa20cc9870e22790d3ec7fa6240a8c')

    depends_on('java', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
