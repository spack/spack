# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


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
    url = "https://pypi.io/packages/source/n/nexusforge/nexusforge-0.6.3.tar.gz"

    version('0.6.3', sha256='ac97247509cf0e12ad4200511e0bd16d4789c0fa39450951ab54dea8c1aa9aa7')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-hjson', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-nexus-sdk', type=('build', 'run'))
    depends_on('py-aiohttp', type=('build', 'run'))
    depends_on('py-pyld', type=('build', 'run'))
    depends_on('py-pyshacl@0.11.6.post1', type=('build', 'run'))
    depends_on('py-rdflib-jsonld@:0.6.099', type=('build', 'run'))
    depends_on('py-rdflib@:5.999', type=('build', 'run'))
    depends_on('py-nest-asyncio@1.5.1:', type=('build', 'run'))
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
