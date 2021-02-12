# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyElasticsearch(PythonPackage):
    """Python client for Elasticsearch"""

    homepage = "https://github.com/elastic/elasticsearch-py"
    pypi = "elasticsearch/elasticsearch-5.2.0.tar.gz"

    version('7.11.0', sha256='1e24b33a82bf381b42d3b0d390f76fdb9d6a9d47b310dea8eaeb0a5933c394c0')
    version('7.10.1', sha256='a725dd923d349ca0652cf95d6ce23d952e2153740cf4ab6daf4a2d804feeed48')
    version('7.10.0', sha256='9053ca99bc9db84f5d80e124a79a32dfa0f7079b2112b546a03241c0dbeda36d')
    version('7.9.1',  sha256='5e08776fbb30c6e92408c7fa8c37d939210d291475ae2f364f0497975918b6fe')
    version('7.9.0',  sha256='813ee0afa9d013ad17a76321c97b2894201fa794fbb03b7c8a1573ba9e607c28')
    version('7.8.1',  sha256='92b534931865a186906873f75ae0b91808ff5036b0f2b9269eb5f6dc09644b55')
    version('7.8.0',  sha256='e637d8cf4e27e279b5ff8ca8edc0c086f4b5df4bf2b48e2f950b7833aca3a792')
    version('7.7.1',  sha256='9bfcb2bd137d6d7ca123e252b9d7261cfe4f7723f7b749a99c52b47766cf387c')
    version('7.7.0',  sha256='35de81968b78a1c708178773ccca56422661fc6e00905b81f48af8e8a9a2a6ba')
    version('7.6.0',  sha256='d228b2d37ac0865f7631335268172dbdaa426adec1da3ed006dddf05134f89c8')
    version('7.5.1', sha256='2a0ca516378ae9b87ac840e7bb529ec508f3010360dd9feed605dff2a898aff5')
    version('6.4.0', sha256='fb5ab15ee283f104b5a7a5695c7e879cb2927e4eb5aed9c530811590b41259ad')
    version('5.2.0', sha256='45d9f8fbe0878a1b7493afeb20f4f6677a43982776ed1a77d9373e9c5b9de966')
    version('2.3.0', sha256='be3080a2bf32dff0a9f9fcc1c087515a25a357645673a976d25ef77166134d81')

    depends_on('py-setuptools', type='build')
    depends_on('py-urllib3@1.8:1.999', type=('build', 'run'))
    # tests_require
    # depends_on('py-requests@1.0.0:2.9.999', type=('build', 'run'))
    # depends_on('py-nose', type=('build', 'run'))
    # depends_on('py-coverage', type=('build', 'run'))
    # depends_on('py-mock', type=('build', 'run'))
    # depends_on('py-pyyaml', type=('build', 'run'))
    # depends_on('py-nosexcover', type=('build', 'run'))
