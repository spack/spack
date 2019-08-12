# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Elasticsearch(Package):
    """Elasticsearch is a search engine based on Lucene. It provides a
    distributed, multitenant-capable full-text search engine with an HTTP web
    interface and schema-free JSON documents.
    """

    homepage = "https://www.elastic.co/"
    url      = "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.4.tar.gz"

    version('6.4.0', '5c23c99a52600b250a6871bf6a744e8b')
    version('6.2.4', '692d01956fe7aee2d08ac0fbf7b7a19e')

    depends_on('jdk', type='run')

    def install(self, spec, prefix):
        dirs = [
            'bin',
            'config',
            'lib',
            'modules',
            'plugins']

        for d in dirs:
            install_tree(d, join_path(prefix, d))
