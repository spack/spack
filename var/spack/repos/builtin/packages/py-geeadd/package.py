# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGeeadd(PythonPackage):
    """Google Earth Engine Batch Assets Manager with Addons."""

    homepage = "https://github.com/samapriya/gee_asset_manager_addon"
    pypi = "geeadd/geeadd-0.3.0.tar.gz"

    version('0.5.3', sha256='e38ee94f0ec660aa9bc371f33d2c6b3177a3c5fccf38459543741689eb26024e')
    version('0.5.2', sha256='3b0dd8607a07eb0993a88c0c907e3ffcdfffec32a811d275e6b6d9d4ed8064eb')
    version('0.5.1', sha256='51a7bfc8ae6ab7cbc8fa00e6424c32be08e1fa3d065ad49b83b753db2b967500')
    version('0.5.0', sha256='f93ef6af3752084db79be8521ddbba5b02b6ccac2788769d7d763ad1d7e36023')
    version('0.4.9', sha256='5b142a1eecc2878b82fc0888b0956d5e826b16835dc275f255ae3724e1922f1c')
    version('0.4.8', sha256='4c6814e937dc45038d696761c74e2a85ba062a25a52c8a1b75800c1c2bbc5b9f')
    version('0.4.7', sha256='6db016b0febf74a351fc37b964b93a7f97263f03edabe745beb112cb35a48e4c')
    version('0.4.6', sha256='4ff2312cf7304c38f5d16daa503c148b898ddb14a7f04f746fe56b61f7d612f6')
    version('0.4.5', sha256='83beca40fcf0cf16c9925a3b0f20bbf8acb282ca13e9031a727c2739d4586f32')
    version('0.4.4', sha256='8f2ba3db5d55f1d7adeabd49d4e42c5726b502dd82f32afc4dd3837d7474fc54')
    version('0.4.3', sha256='8be9cfe89afd766fcf6e88f351d046a762ddf5319335ed72195e62eb19b11b89')
    version('0.4.2', sha256='a544a7c1ad2ca171839bd8c6e4e4d8352e1dbaf225bc70027cf65ce1b0f38c5f')
    version('0.4.1', sha256='51461dae6ff7ffe3854519ef5abed715d3730a1580e9e8a9e14c4bb773e1bc93')
    version('0.4.0', sha256='e74546ff06ebbfa92792d39b404a32b886c913e831d285cdd772cea4feaafc24')
    version('0.3.3', sha256='0210e7c619a987130a2ffb592ec80754db46fa253b29528af0cc7352ecaf236a')
    version('0.3.2', sha256='bdd433eb41561c14bd76860d45b9a7711631676e63177064cae1277bd4c1c7ae')
    version('0.3.1', sha256='e9aac5862a43aeb9ab021f7207ac6e499c4da6a36b2f8081ea609140d0e0055b')
    version('0.3.0', sha256='591e6ff2847122598ed5b0452a892a76e332ce227d4ba75e4d03eca2c7a4beea')

    depends_on('py-setuptools', type='build')
    depends_on('py-earthengine-api@0.1.87:', type=('build', 'run'))
    depends_on('py-requests@2.10.0:', type=('build', 'run'))
    depends_on('py-poster@0.8.1:', type=('build', 'run'))
    depends_on('py-retrying@1.3.3:', type=('build', 'run'))
    depends_on('py-clipboard@0.0.4:', type=('build', 'run'))
    depends_on('py-beautifulsoup4@4.5.1:', type=('build', 'run'))
    depends_on('py-requests-toolbelt@0.7.0:', type=('build', 'run'))
    depends_on('py-future@0.16.0:', type=('build', 'run'))
    depends_on('py-google-cloud-storage@1.1.1:', type=('build', 'run'))
    depends_on('py-oauth2client@4.1.3:', type=('build', 'run'))
