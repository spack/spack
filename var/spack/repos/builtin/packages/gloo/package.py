# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Gloo(CMakePackage, CudaPackage):
    """Gloo is a collective communications library."""

    homepage = "https://github.com/facebookincubator/gloo"
    git      = "https://github.com/facebookincubator/gloo.git"

    version('master', branch='master')
    version('2021-05-04', commit='6f7095f6e9860ce4fd682a7894042e6eba0996f1')  # py-torch@1.9
    version('2020-09-18', commit='3dc0328fe6a9d47bd47c0c6ca145a0d8a21845c6')  # py-torch@1.7:1.8
    version('2020-03-17', commit='113bde13035594cafdca247be953610b53026553')  # py-torch@1.5:1.6
    version('2019-11-05', commit='7c541247a6fa49e5938e304ab93b6da661823d0f')  # py-torch@1.4
    version('2019-09-29', commit='ca528e32fea9ca8f2b16053cff17160290fc84ce')  # py-torch@1.3
    version('2019-06-19', commit='46ae6ec2191a3cc297ab33d4edd43accc35df992')  # py-torch@1.2
    version('2019-02-01', commit='670b4d4aa46886cc66874e2a4dc846f5cfc2a285')  # py-torch@1.0.1:1.1
    version('2018-11-20', commit='cdeb59d5c82e5401445b4c051bb396f6738d4a19')  # py-torch@1.0.0
    version('2018-05-29', commit='69eef748cc1dfbe0fefed69b34e6545495f67ac5')  # py-torch@0.4.1
    version('2018-04-06', commit='aad0002fb40612e991390d8e807f247ed23f13c5')  # py-torch@:0.4.0

    depends_on('cmake@2.8.12:', type='build')
    depends_on('ninja', type='build')

    generator = 'Ninja'

    def cmake_args(self):
        return [self.define_from_variant('USE_CUDA', 'cuda')]
