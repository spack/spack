# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTqdm(PythonPackage):
    """A Fast, Extensible Progress Meter"""

    homepage = "https://github.com/tqdm/tqdm"
    pypi = "tqdm/tqdm-4.45.0.tar.gz"

    version('4.56.2', sha256='11d544652edbdfc9cc41aa4c8a5c166513e279f3f2d9f1a9e1c89935b51de6ff')
    version('4.56.1', sha256='2874fa525c051177583ec59c0fb4583e91f28ccd3f217ffad2acdb32d2c789ac')
    version('4.56.0', sha256='fe3d08dd00a526850568d542ff9de9bbc2a09a791da3c334f3213d8d0bbbca65')
    version('4.55.2', sha256='86ca00c4942c3b3dc7ed31bae44cd2db38ef85ca05a7920f6a6c52ad7fcac904')
    version('4.55.1', sha256='556c55b081bd9aa746d34125d024b73f0e2a0e62d5927ff0e400e20ee0a03b9a')
    version('4.55.0', sha256='f4f80b96e2ceafea69add7bf971b8403b9cba8fb4451c1220f91c79be4ebd208')
    version('4.54.1', sha256='38b658a3e4ecf9b4f6f8ff75ca16221ae3378b2e175d846b6b33ea3a20852cf5')
    version('4.54.0', sha256='5c0d04e06ccc0da1bd3fa5ae4550effcce42fcad947b4a6cafa77bdc9b09ff22')
    version('4.53.0', sha256='3d3f1470d26642e88bd3f73353cb6ff4c51ef7d5d7efef763238f4bc1f7e4e81')
    version('4.52.0', sha256='18d6a615aedd09ec8456d9524489dab330af4bd5c2a14a76eb3f9a0e14471afe')
    version('4.51.0', sha256='ef54779f1c09f346b2b5a8e5c61f96fbcb639929e640e59f8cf810794f406432')
    version('4.50.2', sha256='69dfa6714dee976e2425a9aab84b622675b7b1742873041e3db8a8e86132a4af')
    version('4.50.1', sha256='b04bbbc52a7f1e3665eaa310f34c6ebbdf058bd3f6251fd64c6ab831817121ea')
    version('4.50.0', sha256='93b7a6a9129fce904f6df4cf3ae7ff431d779be681a95c3344c26f3e6c09abfa')
    version('4.49.0', sha256='faf9c671bd3fad5ebaeee366949d969dca2b2be32c872a7092a1e1a9048d105b')
    version('4.48.2', sha256='564d632ea2b9cb52979f7956e093e831c28d441c11751682f84c86fc46e4fd21')
    version('4.48.1', sha256='7b7dd59cd9f03b89365ba67eb8515f5d2803fd1eb707abdbb914691a3123d9df')
    version('4.48.0', sha256='6baa75a88582b1db6d34ce4690da5501d2a1cb65c34664840a456b2c9f794d29')
    version('4.47.0', sha256='63ef7a6d3eb39f80d6b36e4867566b3d8e5f1fe3d6cb50c5e9ede2b3198ba7b7')
    version('4.46.1', sha256='cd140979c2bebd2311dfb14781d8f19bd5a9debb92dcab9f6ef899c987fcf71f')
    version('4.46.0', sha256='4733c4a10d0f2a4d098d801464bdaf5240c7dadd2a7fde4ee93b0a0efd9fb25e')
    version('4.45.0', sha256='00339634a22c10a7a22476ee946bbde2dbe48d042ded784e4d88e0236eca5d81')
    version('4.36.1', sha256='abc25d0ce2397d070ef07d8c7e706aede7920da163c64997585d42d3537ece3d')
    version('4.8.4',  sha256='bab05f8bb6efd2702ab6c532e5e6a758a66c0d2f443e09784b73e4066e6b3a37')

    depends_on('python@2.6:2.8,3.2:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
