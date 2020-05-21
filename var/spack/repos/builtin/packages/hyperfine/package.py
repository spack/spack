# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hyperfine(CargoPackage):
    """A command-line benchmarking tool"""

    homepage  = "https://github.com/sharkdp/hyperfine"
    crates_io = "hyperfine"
    git       = "https://github.com/sharkdp/hyperfine.git"
    
    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('1.9.0', sha256='cf82875c0ec634a287137d18818ac91fbdaf2fe2ecee6598f47a7c6fef48d352')
    version('1.8.0', sha256='09620af8b35e6799ebe7babf51835e4628d650abc7fe7b32dca96f34d3f81f8b')
    version('1.7.0', sha256='4e5af0977e2c091c7ec267a9e7e0cdd8255d075f6ca70bfbc51e116127dbd130')
    version('1.6.0', sha256='36643da44c6d0e149cecae950e2e49098582e29f3dc5e42bbdae8911c76cc9c4')
    version('1.5.0', sha256='1c0d34c50426326a02cf297f73a7ce162dbc5ba3594ed7681cf03eb329b81b37')
    version('1.4.0', sha256='3e587e4e6c9c58ea768c3f0c4f2cb31d24cf24aec97dbf7de84c22e98095fec9')
    version('1.3.0', sha256='be27c9f4d0fe6daa989b18d3dedae19424a4e94884f55fbb303f71c30ea771d8')
    version('1.2.0', sha256='6474ae2388ac0395f99df5f2df5da06dbd3b438f90783008e5f1dfce69e6e2a8')
    version('1.1.0', sha256='a0162201bd466864d9f87518584b5e6ae8f8a45126cc4ffd8fde263d5e62255f')
    version('1.0.0', sha256='086a856d329e0cf0801a9aa562469c3dff3b0202983aa2b84b4f32bbe5bfeb91')
    version('0.5.0', sha256='d9575e044a6dc8972d3eaf701ff2f6d84a2eb9bbf37a28b567f7b9483b7899b5')
    version('0.4.0', sha256='0bd93492c6a209046232416d8b7f84e586e341148ed7d22a227b7af2928550f6')
    version('0.3.0', sha256='5ba014b5663eef867dc2b5826a3fc3735369df669340860f6151a5ef82871ec2')
    version('0.2.0', sha256='b94617e670f6181d790fd47877d8088b38b4b1a1d26ea0dcc8115c1223930bfe')
    version('0.1.0', sha256='ecb1eb4d22ec7dea151354d17f4a98dd3348d9fa64923f42a293c9ac79eaa77b')


