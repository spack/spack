# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ycsb(MavenPackage):
    """Yahoo! Cloud Serving Benchmark."""

    homepage = 'https://research.yahoo.com/news/yahoo-cloud-serving-benchmark/'
    url = 'https://github.com/brianfrankcooper/YCSB/archive/0.17.0.tar.gz'
    git = 'https://github.com/brianfrankcooper/YCSB.git'

    version('master', branch='master')
    version('0.17.0', sha256='5dd1a3d4dd7ac336eadccc83b097c811e142cfe1b23fc278f247054a1892c0e0')
    version('0.16.0', sha256='4296fd5e90d7d6d7dfcbad90039ddf16e785706a07f99c1c8a06e6ee06440f71')
    version('0.15.0', sha256='50b83c11f1a2f19f45e3cc6781f952c69944d1221dfec72169c3587802fc7fbb')
    version('0.14.0', sha256='456bcc9fa3d5d66d76fffa9cec34afd4528d9f02aa8a8d1135f511650516d5cb')
    version('0.13.0', sha256='21cb8078a0fe2d8d909145744ca15848dbb6757e98a7fdc97fb4049f82f4afbc')

    bindings = {
        'accumulo': '0.13.0',
        'accumulo1.6': '0.14.0:0.17.0',
        'accumulo1.7': '0.14.0:0.17.0',
        'accumulo1.8': '0.14.0:0.17.0',
        'accumulo1.9': 'master',
        'aerospike': '0.13.0:',
        'arangodb': '0.13.0:',
        'arangodb3': '0.13.0:0.14.0',
        'asynchbase': '0.13.0:',
        'azurecosmos': '0.16.0:',
        'azuredocumentdb': '0.13.0:0.15.0',
        'azuretablestorage': '0.13.0:',
        'cassandra': '0.13.0:',
        'cloudspanner': '0.13.0:',
        'couchbase': '0.13.0:',
        'couchbase2': '0.13.0:',
        'crail': '0.16.0:',
        'dynamodb': '0.13.0:',
        'elasticsearch': '0.13.0:',
        'elasticsearch5': '0.13.0:',
        'foundationdb': '0.15.0:',
        'geode': '0.13.0:',
        'googlebigtable': '0.13.0:',
        'googledatastore': '0.13.0:',
        'griddb': '0.16.0:',
        'hbase094': '0.13.0',
        'hbase098': '0.13.0:0.17.0',
        'hbase1': 'master',
        'hbase10': '0.13.0:0.17.0',
        'hbase12': '0.13.0:0.17.0',
        'hbase14': '0.14.0:0.17.0',
        'hbase2': 'master',
        'hbase20': '0.14.0:0.17.0',
        'hypertable': '0.13.0:0.17.0',
        'ignite': '0.15.0:',
        'infinispan': '0.13.0:',
        'jdbc': '0.13.0:',
        'kudu': '0.13.0:',
        'mapkeeper': '0.13.0:0.17.0',
        'maprdb': '0.14.0:',
        'maprjsondb': '0.14.0:',
        'memcached': '0.13.0:',
        'mongodb': '0.13.0:',
        'nosqldb': '0.13.0:',
        'orientdb': '0.13.0:',
        'postgrenosql': '0.16.0:',
        'rados': '0.13.0:',
        'redis': '0.13.0:',
        'rest': '0.13.0:',
        'riak': '0.13.0:',
        'rocksdb': '0.15.0:',
        's3': '0.13.0:',
        'scylla': 'master',
        'seaweedfs': 'master',
        'solr': '0.13.0:0.17.0',
        'solr6': '0.13.0:0.17.0',
        'solr7': 'master',
        'tablestore': '0.16.0:master',
        'tarantool': '0.13.0:',
        'voldemort': '0.13.0:0.17.0',
        'voltdb': '0.17.0:',
        'zookeeper': 'master'
    }

    for key in bindings:
        variant_name = key.replace('.', '_') if '.' in key else key
        variant(variant_name, default=False, description='Build the %s binding' % key,
                when='@%s' % bindings[key])

    depends_on('maven@3.1.0:', type='build')
    depends_on('mongodb-async-driver', when='+mongodb', type='build')

    def build(self, spec, prefix):
        mvn = which('mvn')
        if '+mangodb' in spec:
            mongodb_async_driver_version = spec['mongodb-async-driver'].version.string
            jar_name = (
                'target/mongodb-async-driver-' + mongodb_async_driver_version + '.jar'
            )
            path = join_path(self.spec['mongodb-async-driver'].prefix, jar_name)
            mvn(
                'install:install-file',
                '-Dfile={0}'.format(path),
                '-DgroupId=com.allanbank',
                '-DartifactId=mongodb-async-driver',
                '-Dversion=2.0.1',
                '-Dpackaging=jar',
            )
        projects = ['site.ycsb:binding-parent']
        for key in Ycsb.bindings:
            variant_name = key.replace('.', '_') if '.' in key else key
            if '+' + variant_name in spec:
                projects.append('site.ycsb:%s-binding' % key)
        mvn('-pl', ','.join(projects), 'package', '-DskipTests')
