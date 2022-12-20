# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNexusforge(PythonPackage):
    """Blue Brain Nexus Forge is a domain-agnostic, generic and
    extensible Python framework enabling non-expert users to create and
    manage knowledge graphs by making it easy to:
    - Discover and reuse available knowledge resources such as ontologies
    and schemas to shape, constraint, link and add semantics to datasets.
    - Build knowledge graphs from datasets generated from heterogenous
    sources and formats. Defining, executing and sharing data mappers to
    transform data from a source format to a target one conformant to schemas
    and ontologies.
    - Interface with various stores offering knowledge graph storage,
    management and scaling capabilities, for example Nexus Core store or
    in-memory store.
    - Validate and register data and metadata.
    - Search and download data and metadata from a knowledge graph.
    """
    homepage = "https://github.com/BlueBrain/nexus-forge"
    pypi = "nexusforge/nexusforge-0.6.3.tar.gz"

    version('0.8.0', sha256='4358505ead26e41c2a0c4e6113cf3a486c9661e2a3899394497a2b5a94b70424')
    version('0.7.0', sha256='a8d2951d9ad18df9f2f4db31a4c18fcdd27bfcec929b03a3c91f133ea439413c')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.7:', type=('build', 'run'))

    depends_on('py-hjson', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-nexus-sdk', type=('build', 'run'))
    depends_on('py-aiohttp', type=('build', 'run'))
    depends_on('py-pyld', type=('build', 'run'))
    depends_on('py-pyshacl@0.17.2', type=('build', 'run'))
    depends_on('py-rdflib@6.0.0:', type=('build', 'run'))
    depends_on('py-nest-asyncio@1.5.1:', type=('build', 'run'))
    depends_on('py-owlrl@5.2.3:', type=('build', 'run'))
    depends_on('py-pyparsing@2.0.2:', type=('build', 'run'))
    depends_on('py-elasticsearch-dsl@7.4.0:', type=('build', 'run'))
    depends_on('py-scikit-learn', type='run')

    depends_on('py-pytest', type='test')
    depends_on('py-pytest-cov', type='test')
    depends_on('py-tox', type='test')
    depends_on('py-pytest-bdd@3.4.0', type='test')
    depends_on('py-pytest-mock', type='test')
    depends_on('py-codecov', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
