# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCelery(PythonPackage):
    """Celery - Distributed Task Queue."""

    pypi = "celery/celery-4.2.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.2.3",
        sha256="8aacd02fc23a02760686d63dde1eb0daa9f594e735e73ea8fb15c2ff15cb608c",
        url="https://pypi.org/packages/1e/c2/52a01d3f53ddf57c80b011714dd63295c69426121d35d0ff41976b83506c/celery-5.2.3-py3-none-any.whl",
    )

    variant("redis", default=False, description="Use redis transport")
    variant("sqlalchemy", default=False, description="Use sqlalchemy interface")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5:5.3.0")
        depends_on("py-billiard@3.6.4:3", when="@5:5.2")
        depends_on("py-click@8.0.3:", when="@5.2.3:5.2")
        depends_on("py-click-didyoumean@0.0.3:", when="@5:5.2")
        depends_on("py-click-plugins@1.1.1:", when="@5:")
        depends_on("py-click-repl@0.2:", when="@5:")
        depends_on("py-kombu@5.2.3:", when="@5.2.3:5.2")
        depends_on("py-pytz@2021.3:", when="@5.2.3:5.3.0-beta2")
        depends_on("py-redis@3.4.1:4.0.0-rc2,4.0.2:", when="@5.2.3:5.2+redis")
        depends_on("py-setuptools@59.1.1:59.6", when="@5.2.3:5.2.4")
        depends_on("py-sqlalchemy", when="@5:5.2+sqlalchemy")
        depends_on("py-vine@5.0.0:", when="@5:5.3.4")

    # 'auth',
    # 'cassandra',
    # 'django',
    # 'elasticsearch',
    # 'memcache',
    # 'pymemcache',
    # 'couchbase',
    # 'arangodb',
    # 'eventlet',
    # 'rabbitmq'
    # 'gevent',
    # 'msgpack',
    # 'yaml',
    # 'sqs',
    # 'couchdb',
    # 'riak',
    # 'zookeeper',
    # 'solar',
    # 'azureblockblob',
    # 'librabbitmq',
    # 'pyro',
    # 'slmq',
    # 'tblib',
    # 'consul',
    # 'dynamodb',
    # 'mongodb',
    # 'cosmosdbsql',
    # 's3',
