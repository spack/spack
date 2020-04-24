# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DuDust(CargoPackage):
    """A more intuitive version of du"""

    homepage  = "https://github.com/bootandy/dust"
    crates_io = "du-dust"
    git       = "https://github.com/bootandy/dust.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.5.1', sha256='ddfcace4556c7318114307915452698c0aec64465f982c5cac0cdae01630b7a4')
    version('0.5.0', sha256='837e69c3cedf51cde044b4e493be049631b86693ca266fd89394919dd3b7ba5e')
    version('0.4.5', sha256='28e3163026564ca11e6596ee73b327e1d7017f9e119d460a7ab661230d72450a')
    version('0.4.4', sha256='76d6d9744c224d7ca51185e576b4f962aabecae0b038c64dfe541b44df09be25')
    version('0.4.3', sha256='bb2271416acdea31da142856bacf9de37bc1173963ec2b8312ab8b7e0743e4b7')
    version('0.4.2', sha256='d42a0bba2ec1047aaac77f15b419566ad0b46ac32239778bb262c768bb9fc7e5')
    version('0.4.1', sha256='5085b60d1fb27f95fe9551120ce019e31f8d5c99751823844bb737d2de0f6eec')
    version('0.4.0', sha256='a853e79866805644e661fa446cf701ddba8431ae32a6ff3210ceba7880f393f9')
    version('0.3.2', sha256='ba5768ffc4337a63b8b1a25463687f94ca623cb18cbf4451f0c86bab9aa09234')
    version('0.3.1', sha256='bf3fcedeb044bf05bfac52355d95f2e9d83c74536e77e5ee15298a82723231aa')
    version('0.3.0', sha256='213db5967a53456bfdfe205eff71bfd1e93325a10a436e3112facca5ec8225be')
    version('0.2.4', sha256='8cd65839d8248400b250a4322b978ec3ab5a0625609492d7f35e9613d0a61bb1')
