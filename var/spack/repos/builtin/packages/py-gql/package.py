# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyGql(PythonPackage):
    """This is a GraphQL client for Python. Plays nicely with
    graphene, graphql-core, graphql-js and any other GraphQL
    implementation compatible with the spec.
    GQL architecture is inspired by React-Relay and Apollo-Client."""

    homepage = "https://github.com/graphql-python/gql"
    url      = "https://github.com/graphql-python/gql/archive/v3.0.0a1.tar.gz"

    version('3.0.0a1', sha256='3254a6010464932e3700a8d225cf6e40a6983aaf5f279615504c8196a374daf9')
    version('0.4.0', sha256='bd27c44b15b529fecdd80b07291dfd40264a2af937a75b41ff2be49a730e41d8',
            deprecated=True)

    depends_on('py-setuptools', type='build')
    depends_on('py-aiohttp@3.6.2', type=('build', 'run'), when='@3.0:')
    depends_on('py-graphql-core@3.1.0:3.1.999', type=('build', 'run'), when='@3.0:')
    depends_on('py-requests@2.23:2.999', type=('build', 'run'), when='@3.0:')
    depends_on('py-websockets@8.1:8.999', type=('build', 'run'), when='@3.0:')
    depends_on('py-yarl@1.4:1.999', type=('build', 'run'), when='@3.0:')

    depends_on('py-graphql-core@2.0:2.9', type=('build', 'run'), when='@0.4.0')
    depends_on('py-six@1.10.0:', type=('build', 'run'), when='@0.4.0')
    depends_on('py-promise@2.0:3', type=('build', 'run'), when='@0.4.0')
    depends_on('py-requests@2.12:2.999', type=('build', 'run'), when='@0.4.0')
