# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class PyGraphqlCore(PythonPackage):
    """GraphQL-core 3 is a Python 3.6+ port of GraphQL.js, the
    JavaScript reference implementation for GraphQL, a query language
    for APIs created by Facebook."""

    homepage = "https://github.com/graphql-python/graphql-core"
    pypi     = "graphql-core/graphql-core-3.1.5.tar.gz"

    version('3.1.2', sha256='c056424cbdaa0ff67446e4379772f43746bad50a44ec23d643b9bdcd052f5b3a')
    version('3.0.5', sha256='51f7dab06b5035515b23984f6fcb677ed909b56c672152699cca32e03624992e')
    version('2.3.2', sha256='aac46a9ac524c9855910c14c48fc5d60474def7f99fd10245e76608eba7af746')

    depends_on('python@3.6:3', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
