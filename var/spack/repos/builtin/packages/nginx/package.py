# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nginx(AutotoolsPackage):
    """nginx [engine x] is an HTTP and reverse proxy server, a mail proxy
    server, and a generic TCP/UDP proxy server, originally written by Igor
    Sysoev."""

    homepage = "https://nginx.org/en/"
    url      = "https://nginx.org/download/nginx-1.12.0.tar.gz"

    version('1.19.6',  sha256='b11195a02b1d3285ddf2987e02c6b6d28df41bb1b1dd25f33542848ef4fc33b5')
    version('1.19.5',  sha256='5c0a46afd6c452d4443f6ec0767f4d5c3e7c499e55a60cd6542b35a61eda799c')
    version('1.19.4',  sha256='61df546927905a0d624f9396bb7a8bc7ca7fd26522ce9714d56a78b73284000e')
    version('1.19.3',  sha256='91e5b74fa17879d2463294e93ad8f6ffc066696ae32ad0478ffe15ba0e9e8df0')
    version('1.19.2',  sha256='7c1f7bb13e79433ee930c597d272a64bc6e30c356a48524f38fd34fa88d62473')
    version('1.19.1',  sha256='a004776c64ed3c5c7bc9b6116ba99efab3265e6b81d49a57ca4471ff90655492')
    version('1.19.0',  sha256='44a616171fcd7d7ad7c6af3e6f3ad0879b54db5a5d21be874cd458b5691e36c8')
    version('1.18.0',  sha256='4c373e7ab5bf91d34a4f11a0c9496561061ba5eee6020db272a17a7228d35f99')
    version('1.17.10', sha256='a9aa73f19c352a6b166d78e2a664bb3ef1295bbe6d3cc5aa7404bd4664ab4b83')
    version('1.17.9',  sha256='7dd65d405c753c41b7fdab9415cfb4bdbaf093ec6d9f7432072d52cb7bcbb689')
    version('1.17.8',  sha256='97d23ecf6d5150b30e284b40e8a6f7e3bb5be6b601e373a4d013768d5a25965b')
    version('1.17.7',  sha256='b62756842807e5693b794e5d0ae289bd8ae5b098e66538b2a91eb80f25c591ff')
    version('1.17.6',  sha256='3cb4a5314dc0ab0a4e8a7b51ae17c027133417a45cc6c5a96e3dd80141c237b6')
    version('1.17.5',  sha256='63ee35e15a75af028ffa1f995e2b9c120b59ef5f1b61a23b8a4c33c262fc10c3')
    version('1.17.4',  sha256='62854b365e66670ef4f1f8cc79124f914551444da974207cd5fe22d85710e555')
    version('1.17.3',  sha256='3b84fe1c2cf9ca22fde370e486a9ab16b6427df1b6ea62cdb61978c9f34d0f3c')
    version('1.17.2',  sha256='5e333687464e1d6dfb86fc22d653b99a6798dda40093b33186eeeec5a97e69ec')
    version('1.17.1',  sha256='6f1825b4514e601579986035783769c456b888d3facbab78881ed9b58467e73e')
    version('1.17.0',  sha256='e21b5d06cd53e86afb94f0b3678e0abb0c0f011433471fa3d895cefa65ae0fab')
    version('1.16.1',  sha256='f11c2a6dd1d3515736f0324857957db2de98be862461b5a542a3ac6188dbe32b')
    version('1.16.0',  sha256='4fd376bad78797e7f18094a00f0f1088259326436b537eb5af69b01be2ca1345')
    version('1.15.12', sha256='3d5b90aa17de1700709ae4ec6c4d73d87c888b06c510391bf7104b006fdb2abe')
    version('1.15.11', sha256='d5eb2685e2ebe8a9d048b07222ffdab50e6ff6245919eebc2482c1f388e3f8ad')
    version('1.15.10', sha256='b865743abd52bce4745d0f7e7fedde3cafbaaab617b022c105e3e4e456537c3c')
    version('1.15.9',  sha256='e4cfba989bba614cd53f3f406ac6da9f05977d6b1296e5d20a299f10c2d7ae43')
    version('1.15.8',  sha256='a8bdafbca87eb99813ae4fcac1ad0875bf725ce19eb265d28268c309b2b40787')
    version('1.15.7',  sha256='8f22ea2f6c0e0a221b6ddc02b6428a3ff708e2ad55f9361102b1c9f4142bdf93')
    version('1.15.6', sha256='a3d8c67c2035808c7c0d475fffe263db8c353b11521aa7ade468b780ed826cc6')
    version('1.13.8', sha256='8410b6c31ff59a763abf7e5a5316e7629f5a5033c95a3a0ebde727f9ec8464c5')
    version('1.12.0', sha256='b4222e26fdb620a8d3c3a3a8b955e08b713672e1bc5198d1e4f462308a795b30')

    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')

    conflicts('%gcc@8:', when='@:1.14')

    def configure_args(self):
        args = ['--with-http_ssl_module']
        return args

    def setup_run_environment(self, env):
        """Prepend the sbin directory to PATH."""
        env.prepend_path('PATH', self.prefix.sbin)
