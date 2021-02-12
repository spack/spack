# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIsort(PythonPackage):
    """A Python utility / library to sort Python imports."""

    homepage = "https://github.com/timothycrosley/isort"
    pypi = "isort/isort-4.2.15.tar.gz"

    version('5.7.0',  sha256='c729845434366216d320e936b8ad6f9d681aab72dc7cbc2d51bedc3582f3ad1e')
    version('5.6.4',  sha256='dcaeec1b5f0eca77faea2a35ab790b4f3680ff75590bfcb7145986905aab2f58')
    version('5.6.3',  sha256='3820dd92c3214290cda6351f2ae2cedd5170759bc434af600eaad4f7a82a6ade')
    version('5.6.2',  sha256='c2cfe5b621f62932677004f96f93c4b128dc457d957b0531f204641fe8adc8a6')
    version('5.6.1',  sha256='2f510f34ae18a8d0958c53eec51ef84fd099f07c4c639676525acbcd7b5bd3ff')
    version('5.6.0',  sha256='20544581447ccb6a80940c5cace8cbc32c0f58d82d67d34a182950fe7b93321b')
    version('5.5.5',  sha256='47e0fdc03aed3a9ba507284f90e4b3b6f2a4725d919816a7b547675befc38ffb')
    version('5.5.4',  sha256='ba040c24d20aa302f78f4747df549573ae1eaf8e1084269199154da9c483f07f')
    version('5.5.3',  sha256='6187a9f1ce8784cbc6d1b88790a43e6083a6302f03e9ae482acc0f232a98c843')
    version('5.5.2',  sha256='171c5f365791073426b5ed3a156c2081a47f88c329161fd28228ff2da4c97ddb')
    version('5.5.1',  sha256='92533892058de0306e51c88f22ece002a209dc8e80288aa3cec6d443060d584f')
    version('5.5.0',  sha256='0906e0e7092e060c05de709ad172e1ec1b26aa27fdd4e8093f257890cd881d18')
    version('5.4.2',  sha256='d488ba1c5a2db721669cc180180d5acf84ebdc5af7827f7aaeaa75f73cf0e2b8')
    version('5.4.1',  sha256='a4fb5fffc46494cda15e33a996c8e724f8e3db19682b84cc7c990b57f2941e9f')
    version('5.4.0',  sha256='2426f423a77bfb639ec67cf13ef7cb96f3521772b8831f099a777aae0c9ba571')
    version('5.3.2',  sha256='ba83762132a8661d3525f87a86549712fb7d8da79eeb452e01f327ada9e87920')
    version('5.3.1',  sha256='b9b54475340302a69b036e5ecb3576d42f7e8118f33ba9a6c385765dc42072b0')
    version('5.3.0',  sha256='cdca22530d093ed16983ba52c41560fa0219d1b958e44fd2ae2995dcc7b785be')
    version('5.2.2',  sha256='96b27045e3187b9bdde001143b79f9b10a462f372bff7062302818013b6c86f3')
    version('5.2.1',  sha256='761a8f490d8bbcd3549b5618ed423468bbdece603cce44b290ee274c9a360893')
    version('5.2.0',  sha256='27c7f27adc4b1a6afde1b66c8af46d42da03671d68648e2a8ab2166df03b668e')
    version('5.1.4',  sha256='145072eedc4927cc9c1f9478f2d83b2fc1e6469df4129c02ef4e8c742207a46c')
    version('5.1.3',  sha256='9be41d107294ddf25ef6af83979cb3dfa1b5752311b6d50611c8f8d321d4a4eb')
    version('5.1.2',  sha256='64022dea6a06badfa09b300b4dfe8ba968114a737919e8ed50aea1c288f078aa')
    version('5.1.1',  sha256='069aa3af9b51c7f67311710e70514e685e868cd71cc1c39e78a5264f0d048c1e')
    version('5.1.0',  sha256='b19b7ebce5e292507afa8fab30dd666011dd5ae8f4ef2a2d431751dc84c22140')
    version('5.0.9',  sha256='639b8084644ceb13a806f42d690273b9d844793ac2f515fbc575ba65dc044de0')
    version('5.0.8',  sha256='7c4bd2f833a402dff55cb30c7e570ac4f14ec94d571e2eac56a48ee3856faf48')
    version('5.0.7',  sha256='6bc0b408d7c62e331d355085914dd28fd352635f6babd5e4605702ff3b6d9c09')
    version('5.0.6',  sha256='af3ac4524d1256e3f32d155da8fb43b2a94201644fa6b45813c8783fc51c3841')
    version('5.0.5',  sha256='cb76a2fac5ac08eae0020f7e56bab895cf3d8982034aa16f3cd67984edf26223')
    version('5.0.4',  sha256='6ae9cf5414e416954e3421f861cbbfc099b3ace63cb270cc76c6670efd960a0a')
    version('5.0.3',  sha256='4c48d4cd773a6226baaaa176839e6f7ff82ef7c7842f6c54374fe2b14df4024b')
    version('5.0.2',  sha256='ba8e494fc13974ec02a623c4aaead306bb86a3102a1df8d399748445f32a78f2')
    version('5.0.1',  sha256='eae6ecb60a336da7abd9695e43e603230348b317dc516a73656623e604b95732')
    version('5.0.0',  sha256='96afb994c4c6f2cb52974363ea56881942a70b57029d2f750e1009921a5b3aa2')
    version('4.3.21', sha256='54da7e92468955c4fceacd0c86bd0ec997b0e1ee80d97f67c35a78b719dccab1')
    version('4.3.20', sha256='c40744b6bc5162bbb39c1257fe298b7a393861d50978b565f3ccd9cb9de0182a')
    version('4.2.15', sha256='79f46172d3a4e2e53e7016e663cc7a8b538bec525c36675fcfd2767df30b3983')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'), when='@4.3.0:')
    depends_on('py-futures', type=('build', 'run'), when='@4.3.0: ^python@:3.1')
    depends_on('py-backports-functools-lru-cache', type=('build', 'run'), when='@4.3.10: ^python@:3.1')
