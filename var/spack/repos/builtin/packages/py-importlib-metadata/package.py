# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImportlibMetadata(PythonPackage):
    """Read metadata from Python packages."""

    homepage = "https://importlib-metadata.readthedocs.io/"
    pypi = "importlib_metadata/importlib_metadata-1.2.0.tar.gz"

    version('3.4.0', sha256='fa5daa4477a7414ae34e95942e4dd07f62adf589143c875c133c1e53c4eff38d')
    version('3.3.0', sha256='5c5a2720817414a6c41f0a49993908068243ae02c1635a228126519b509c8aed')
    version('3.2.0', sha256='8f3c7e27824aa3283b384ee1f9238770e4fafe479150fa7012830dfae110e7d0')
    version('3.1.1', sha256='b0c2d3b226157ae4517d9625decf63591461c66b3a808c2666d538946519d170')
    version('3.1.0', sha256='d9b8a46a0885337627a6430db287176970fff18ad421becec1d64cfc763c2099')
    version('3.0.0', sha256='d582eb5c35b2f16c78e365e0f89e369f36af38fdaad0146208aa973c693ba247')
    version('2.1.1', sha256='b8de9eff2b35fb037368f28a7df1df4e6436f578fa74423505b6c6a778d5b5dd')
    version('2.1.0', sha256='caeee3603f5dcf567864d1be9b839b0bcfdf1383e3e7be33ce2dead8144ff19c')
    version('2.0.0', sha256='77a540690e24b0305878c37ffd421785a6f7e53c8b5720d211b211de8d0e95da')
    version('1.2.0', sha256='41e688146d000891f32b1669e8573c57e39e5060e7f5f647aa617cd9a9568278')
    version('0.23',  sha256='aa18d7378b00b40847790e7c27e11673d7fed219354109d0e7b9e5b25dc3ad26')
    version('0.19',  sha256='23d3d873e008a513952355379d93cbcab874c58f4f034ff657c7a87422fa64e8')
    version('0.18',  sha256='cb6ee23b46173539939964df59d3d72c3e0c1b5d54b84f1d8a7e912fe43612db')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-zipp@0.5:', type=('build', 'run'))
    depends_on('py-pathlib2', when='^python@:2', type=('build', 'run'))
    depends_on('py-contextlib2', when='^python@:2', type=('build', 'run'))
    depends_on('py-configparser@3.5:', when='^python@:2', type=('build', 'run'))
