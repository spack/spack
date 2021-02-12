# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyStevedore(PythonPackage):
    """Manage Dynamic Plugins for Python Applications."""

    homepage = "https://docs.openstack.org/stevedore/latest/"
    pypi = "stevedore/stevedore-1.28.0.tar.gz"

    version('3.3.0',  sha256='3a5bbd0652bf552748871eaa73a4a8dc2899786bc497a2aa1fcb4dcdb0debeee')
    version('3.2.2',  sha256='f845868b3a3a77a2489d226568abe7328b5c2d4f6a011cc759dfa99144a521f0')
    version('3.2.1',  sha256='a34086819e2c7a7f86d5635363632829dab8014e5fd7be2454c7cba84ac7514e')
    version('3.2.0',  sha256='38791aa5bed922b0a844513c5f9ed37774b68edc609e5ab8ab8d8fe0ce4315e5')
    version('3.1.0',  sha256='79270bd5fb4a052e76932e9fef6e19afa77090c4000f2680eb8c2e887d2e6e36')
    version('3.0.0',  sha256='182d557078b4f840f412f148e6f3c2ace83a3e206a020f35f6c97d3b8d91f180')
    version('2.0.1',  sha256='609912b87df5ad338ff8e44d13eaad4f4170a65b79ae9cb0aa5632598994a1b7')
    version('2.0.0',  sha256='001e90cd704be6470d46cc9076434e2d0d566c1379187e7013eb296d3a6032d9')
    version('1.32.0', sha256='18afaf1d623af5950cc0f7e75e70f917784c73b652a34a12d90b309451b5500b')
    version('1.31.0', sha256='e0739f9739a681c7a1fda76a102b65295e96a144ccdb552f2ae03c5f0abe8a14')
    version('1.30.1', sha256='7be098ff53d87f23d798a7ce7ae5c31f094f3deb92ba18059b1aeb1ca9fec0a0')
    version('1.30.0', sha256='b92bc7add1a53fb76c634a178978d113330aaf2006f9498d9e2414b31fbfc104')
    version('1.29.0', sha256='1e153545aca7a6a49d8337acca4f41c212fbfa60bf864ecd056df0cafb9627e8')
    version('1.28.0', sha256='f1c7518e7b160336040fee272174f1f7b29a46febb3632502a8f2055f973d60b')

    depends_on('python@2.6:')

    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-pbr@2.0.0:2.1.0', type=('build', 'run'))
