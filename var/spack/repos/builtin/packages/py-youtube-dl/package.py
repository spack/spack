# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyYoutubeDl(PythonPackage):
    """Command-line program to download videos from YouTube.com and other video
    sites."""

    homepage = "https://github.com/ytdl-org/youtube-dl"
    pypi = "youtube_dl/youtube_dl-2020.3.24.tar.gz"

    version('2021.2.10',    sha256='b390cddbd4d605bd887d0d4063988cef0fa13f916d2e1e3564badbb22504d754')
    version('2021.2.4.1',   sha256='b337f20563094decc6b3c16e6fcad14ec3df9d99519344d6e95e40878b2c8075')
    version('2021.2.4',     sha256='16a5e57a24e56bd3557b57bc8c438efa23a13aeff7ce7a04941c5e307f8148bb')
    version('2021.1.24.1',  sha256='d0dc8abd6e89f81171c66d2ffc073eaabf9d5fc6de94e244da36f92a75cc52d7')
    version('2021.1.16',    sha256='acf74701a31b6c3d06f9d4245a46ba8fb6c378931681177412043c6e8276fee7')
    version('2021.1.8',     sha256='1a216c0172b145e7231e8f87f66dc914dce996f993920857b77996fa04e6290c')
    version('2021.1.3',     sha256='67cc185783ef828249bcc199317a207d19e1320857bb16e68d64ea97ad2793b3')
    version('2020.12.31',   sha256='173fca869f8d2a6008cd7d13627f368adc1f334e973f49f03a3fe62b16ac2fea')
    version('2020.12.29',   sha256='98bd918182b88930ee40c4f67926d2c2c15731df3807721c37c4a7914457484c')
    version('2020.12.26',   sha256='c937430888669a90315f11fa3754961aa4b472c6e217950c64141ec112090db7')
    version('2020.12.22',   sha256='fc5368f34e6db3ebeda6071e65eff9490a01722537626f535b7b7b302148b999')
    version('2020.12.14',   sha256='eaa859f15b6897bec21474b7787dc958118c8088e1f24d4ef1d58eab13188958')
    version('2020.12.12',   sha256='a57bab1cfc3d57ae84e26e735daac498fd7b54261fe911e5ba58acfd0ed71742')
    version('2020.12.9',    sha256='cf32d3e106a63d1519c54a2c39aae449031dd1e18a5a443786c2feb5ab842e6b')
    version('2020.12.7',    sha256='bd127c3251a8e9f7a0eb18e4bbcf98409c0365354f735c985325bc19af669a24')
    version('2020.12.5',    sha256='c73c79ccaabb7eabc223b36889ad9d3fbe04433d933312e8752d6a2c2bdc028d')
    version('2020.12.2',    sha256='bc82acb0b59b25b822fad85bef0cbe78e5754ca532e3bd6899fe06386e2b8e7c')
    version('2020.11.29',   sha256='849d2a85ee99e5caafc8d52572bb603c4ae020dfb615a4d51c3bc90787d40df3')
    version('2020.11.26',   sha256='3d52d2c969ec9521a086c43f809fd7545708b7ba24d7379fb123b5438ba691e1')
    version('2020.11.24',   sha256='f701befffe00ae4b0d56f88ed45e1295c151c340d0011efdb1005012abc81996')
    version('2020.11.21.1', sha256='a785c1373a3c2d0b82c54aabc4831e8e6f6ede059ec462e54526d694dd3c29ca')
    version('2020.11.21',   sha256='cc8db451a2baab3e9802dec4e7347ea728759c344913b3b015bc113370a36dca')
    version('2020.11.19',   sha256='2d6adbf7643467fa448939ebe6bebb002071b11dadf545909ca973f101b2584c')
    version('2020.11.18',   sha256='fd879801004d80d875680041d8dcba25bd36cfdaeb0ca704607f16b3709a4f21')
    version('2020.11.17',   sha256='933519ab7d2fa05bd28f8443a2115d21efd0355c051986548af9f233e300db0b')
    version('2020.11.12',   sha256='1491df1707f47207bfd47dd8497d26e9125dd9e4fe2e00780103d4c1b4b2088d')
    version('2020.11.1.1',  sha256='b73379d6b08f03aec49a1899affe4cfd35bb92002dbdb3a3a1435a5811d4f120')
    version('2020.11.1',    sha256='4c97edc8ff18b9449f6244d75095f68d7940ed68afc10c7e0ae4c7f1d753df4f')
    version('2020.9.20',    sha256='67fb9bfa30f5b8f06227c478a8a6ed04af1f97ad4e81dd7e2ce518df3e275391')
    version('2020.9.14',    sha256='fdd7e328c6f23e83f331490293dc8fb4d4ca07eaf22b895d51021541abcc4236')
    version('2020.9.6',     sha256='eced5195e3264c36d2d62610bf235f75b592d5bb2f8ac424fd8da54ee426cd75')
    version('2020.7.28',    sha256='4af90dac41dba8b2c8bdce3903177c4ecbc27d75e03a3f08070f9d9decbae829')
    version('2020.6.16.1',  sha256='9fc0389a1bbbeb609a5bb4ad5630dea107a9d1a24c73721c611a78c234309a75')
    version('2020.6.16',    sha256='bb89ac33b360a4d7f4438dd1cdcf6e94fd092af99e4f012f73e9fb9b80e8e82f')
    version('2020.6.6',     sha256='74e6cc7395060fc39f0b8e21c1e4707486da904c96145bd875187bda2da83b04')
    version('2020.5.29',    sha256='1a3d84afa851dce2fccc2dfc0f9ffa0e22314ffba6d528b34b4a7fe3e0cf2264')
    version('2020.5.8',     sha256='22da6788b55b7b267c6d59bcdfaf10e67a9ac980976d50d29a670473ad2a05bb')
    version('2020.5.3',     sha256='e7a400a61e35b7cb010296864953c992122db4b0d6c9c6e2630f3e0b9a655043')
    version('2020.3.24', sha256='4b03efe439f7cae26eba909821d1df00a9a4eb82741cb2e8b78fe29702bd4633')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('ffmpeg+openssl', type='run')
