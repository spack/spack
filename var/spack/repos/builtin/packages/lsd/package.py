# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lsd(CargoPackage):
    """
    LSD (LSDeluxe)

    The next gen ls command
    """

    homepage = "https://github.com/peltoche/lsd"

    # Pull directly from crates.io for published releases
    crates_io = "lsd"
    # Can install master branch from GitHub
    git = "https://github.com/peltoche/lsd.git"

    version('master', branch='master')
    version('0.17.0', sha256='d1e376b5db9c01304b4545f03d642ac5fa480289f060d014b1cec3a0df2c3990')
    version('0.16.0', sha256='24e8de459c1f2161fc782b6dd22d9862d60b394309344a5ab2281fa94e1a0902')
    version('0.15.1', sha256='b6550b8c875a1fe3f07a6ef670384e9b2140417c682e7f3bfde4eb3ae36f3a75')
    version('0.15.0', sha256='393763deff07cfb5dafa287e169e1936f5013e8ab63bba9ab4afd80df4057164')
    version('0.14.0', sha256='2126cea7c942d4469870eda5a2157d1a66eccf38ad4389b9d2880879e6318cab')
    version('0.13.0', sha256='4972b4a27d5ae97bc87ffc3412da3364c0b3b23c08d47985f45f87f3ad3a97a5')
    version('0.12.0', sha256='078e4d14597c00ace659f6de04bd8bab24bbc37163e996e45dda42c45b510751')
    version('0.11.1', sha256='f80efd3dafe8f6dceb183d51d9d59d906892d496c53de5faa554be7833e00f79')
    version('0.11.0', sha256='43b9360d629aa1b2fd8d30e56be9e58d543d28ff1c6aebdf58e9b9cfff064e38')
    version('0.10.0', sha256='a4cd8460bf320875b14b029c5b3756f59cba0c61dda267663c162c34ce032625')
    version('0.9.0',  sha256='f16de75203269be5918254f7a3ccfb03a93f0e94395adbdd5f2a0a11de30bd3b')
    version('0.8.0',  sha256='3d45e7f853b310904797568bd27a3170caffeb1d364ae9011b8909eda11e5d50')
    version('0.7.12', sha256='b605366341dcc5dc4b25c8903e88058e6757c21e9bda3c718b8f54faf2358d0c')
    version('0.7.11', sha256='ef190786a4b492ccc986efe258af6c19a0695bf8291a0f4e919df5e7aa73d936')
    version('0.7.10', sha256='8679cfee1e7228fa5a2ffdb540eea2f279f2ad287acc6b141325c87f89de8f7c')
    version('0.7.9',  sha256='6ac3428f5b9c3cbd98c66c1ab37594a0b9214ac3f45ec1a7804df4b2833805f6')
    version('0.7.8',  sha256='342e21ad94ee2b88aff28996e50d8c2c61082119c00fc34356e6e905023de1b4')
    version('0.7.7',  sha256='5a8836fc55cc27a6f76f8767e65d3e5d9522f437be5d1a3dc95e9888c0275406')
    version('0.7.6',  sha256='5996b1882c578b68623ea3f574aa1c857e16a0a627504e0a31f2eb6193c5d117')
    version('0.7.5',  sha256='42ca2f2887b6a452142a5856d844206c605e1af8e60092cdab3213c33e5c8612')
    version('0.7.4',  sha256='b0c1cee8789299ae09e28cac3fbd69881197650f0d7561f90e4200b703a07334')
    version('0.7.3',  sha256='46a18dc0dd8c1e7c6f23c87beaa142fd59f7ef71bb6336f640a1961919d9a88c')
    version('0.7.2',  sha256='fe23de3b6058d0ffb648027069aaece58d4060b1d274951b87b4ee7b55549d07')
    version('0.7.1',  sha256='bd35b010cc03c6ca38b287f04f293638bfac18c73e453f2b7a4cf9aabd1ccac0')
    version('0.7.0',  sha256='ae14af5880ca22ccd2e72af49632e3b015e77d31539cdd5cc5c91d59759465a5')
    version('0.6.4',  sha256='e7c9996679afaca801fcc00730d3e452f4ceb2cd4bcd03afbe0cb01ea0f421ce')
    version('0.6.3',  sha256='981f13acf8d20d3e4b1a5a4702124c3169a29a1b2a0f70c5c9e7a0e67af5ec13')
    version('0.6.2',  sha256='d128e75e44bbd77e6e25d7efd9763f91274a593c2b704bf2ed22b6740f9bc1c7')
    version('0.6.1',  sha256='64abc39c19e9e0acebe674ae5c083fe9b55d4f770844dd320d75490aca6df602')
    version('0.6.0',  sha256='963d3de1f66572ed96da2c869fa641ba6c921b0c3e5d56764b0e8d96eff7aa63')
    version('0.5.0',  sha256='0a82228b3dc9ffaea2578e6305a551204cdce7299caece23a1d6ff9e05efeb23')
    version('0.4.1',  sha256='c724f675cc24f7b0754f527a9711afafaa7b49b2f6707ec2a934f311efbef564')
    version('0.4.0',  sha256='0e26149d560be31fd30e6f69663fdc425d24bf8f588211d6ecb1bdce6a7806b1')
    version('0.3.1',  sha256='ae88894e29288c140924c48beaf5cb6bb4c019e341b6bc87bf7dcdbb81ff6e47')
    version('0.3.0',  sha256='d19bf75b4da70b55fc98a4f003f1268bdc8beb470cb3ce3f5ec76adbba96e8d9')
    version('0.2.0',  sha256='f35c7bc11526316b749dccc4e3dfd4b684d83412f8a6f0fc83a7897ff7b5a539')
    version('0.1.0',  sha256='ba47919da7044ba343007de1458a881e1d46e5036a16c39032ea60474a8ba9b9')
