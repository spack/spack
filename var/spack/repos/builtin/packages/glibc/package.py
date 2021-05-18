# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glibc(AutotoolsPackage, GNUMirrorPackage):
    """The GNU C Library provides many of the low-level components used
    directly by programs written in the C or C++ languages."""

    homepage        = "https://www.gnu.org/software/libc/"
    gnu_mirror_path = "libc/glibc-2.33.tar.gz"
    git             = "https://sourceware.org/git/glibc.git"
    maintainers     = ['haampie']

    build_directory = 'build'

    version('master', branch='master')
    version('2.33',   sha256='ad7dbed6b0cde9ddc90e84856da7e2c1f976a5e791cdee947d8dbb0392fc76cf')
    version('2.32',   sha256='f52e5bdc6607cb692c0f7134b75b3ba34b5121628a1750c03e3c9aa0b9d9e65a')
    version('2.31',   sha256='cb2d64fb808affff30d8a99a85de9d2aa67dc2cbac4ae99af4500d6cfea2bda7')
    version('2.30',   sha256='decb0a29f1410735bed0e8e7247361da2bbf0dcfef7ac15bf26e7f910cb964c0')
    version('2.29',   sha256='2fc8c555fd0e5dab5b91e7dd0422865c1885be89ff080b2c1357041afbbc717f')
    version('2.28',   sha256='f318d6e3f1f4ed0b74d2832ac4f491d0fb928e451c9eda594cbf1c3bee7af47c')
    version('2.27',   sha256='881ca905e6b5eec724de7948f14d66a07d97bdee8013e1b2a7d021ff5d540522')
    version('2.26',   sha256='dcc2482b00fdb1c316f385f8180e182bbd37c065dc7d8281a4339d2834ef1be7')
    version('2.25',   sha256='ad984bac07844ecc222039d43bd5f1f1e1571590ea28045232ae3fa404cefc32')
    version('2.24',   sha256='7e01959a42d37739e40d8ce58f9c14750cc68bc8a8669889ed586f9f03b91fbe')
    version('2.23',   sha256='2bd08abb24811cda62e17e61e9972f091f02a697df550e2e44ddcfb2255269d2')
    version('2.22',   sha256='a62610c4084a0fd8cec58eee12ef9e61fdf809c31e7cecbbc28feb8719f08be5')
    version('2.21',   sha256='8d8f78058f2e9c7237700f76fe4e0ae500db31470290cd0b8a9739c0c8ce9738')
    version('2.20',   sha256='37e1de410d572a19b707b99786db9822bb4775e9d70517d88937ab12e6d6debc')
    version('2.19',   sha256='18ad6db70724699d264add80b1f813630d0141cf3a3558b4e1a7c15f6beac796')
    version('2.18',   sha256='c8e727b5feef883184241a4767725ec280c0288794bc5cd4432497370db47734')
    version('2.17',   sha256='a3b2086d5414e602b4b3d5a8792213feb3be664ffc1efe783a829818d3fca37a')
    version('2.16.0', sha256='a75be51658cc1cfb6324ec6dbdbed416526c44c14814823129f0fcc74c279f6e')
    version('2.15',   sha256='da6b95d14b722539c2ec02e7ae1221318dba3d27f19c098a882ffa71bb429c20')
    version('2.14.1', sha256='f80c40897df49c463a6d5a45f734acbfe1bf42ef209a92a5c217aeb383631bdb')
    version('2.14',   sha256='4812ddcedb5270869ef97c165980af5b459f3986dd5d420a5eb749171c8facec')
    version('2.13',   sha256='bd90d6119bcc2898befd6e1bbb2cb1ed3bb1c2997d5eaa6fdbca4ee16191a906')
    version('2.12.2', sha256='6b7392a7b339a3f2db6e4bc8d5418cf29116d9e7e36b313e845cb65e449c5346')
    version('2.12.1', sha256='5ae2edf67169aac932a281cbe636f8be42a854cc3d8b7f325c53b949eab72d48')
    version('2.11.3', sha256='ddc3210f4029991f5142fda7f269f9bfb197917e5d9445ba2d90d31f74cc2765')
    version('2.11.2', sha256='3724ad03a992ed13b75c4d1db54cfe8d059f0a2a028880c1518f3393da44baf6')
    version('2.11.1', sha256='9acf4109333d53073478d95db7a010c1dda47bc6218db1045a062b5e3c1a3c6b')
    version('2.11',   sha256='2ff2cc82616dd5eb9bb8f8e77b0a2cfd1fba9cb4762a5900636fbcfe0160ac15')
    version('2.10.1', sha256='cd9743db33389e7b4eb2942a4f365d12fc015f115113b230152280c43ccc7e3f')
    version('2.9',    sha256='e0210dec2a4ca0a03d8ee26e2a4ebccc915d99f4cdb1489ff0f9f4ce7bda3e30')
    version('2.8',    sha256='a5b91339355a7bbafc5f44b524556f7f25de83dd56f2c00ef9240dabd6865663')
    version('2.7',    sha256='f5ef515cb70f8d4cfcee0b3aac05b73def60d897bdb7a71f4356782febfe415a')
    version('2.6.1',  sha256='6be7639ccad715d25eef560ce9d1637ef206fb9a162714f6ab8167fc0d971cae')
    version('2.6',    sha256='7a50a235c39cf390790f09b9b335eb1e21de8125ab126c4c97e01f66d8865676')
    version('2.5.1',  sha256='36bdbfcc6c5f52bbe5b0f2d327fadcd647c7d3675266b9b933f3888649240d1c')
    version('2.5',    sha256='16d3ac4e86eed75d85d80f1f214a6bd58d27f13590966b5ad0cc181df85a3493')
    version('2.4',    sha256='641877b54c539cacb7d929cf552f5cc961fc2d7da5da54e9d884cf9da13afde7')
    version('2.3.6',  sha256='181237a9f12293acfb84efa3633dab2514193540be261de1d4ee15fd92ba66cd')
    version('2.3.5',  sha256='7ad3ac2e3568456cf03fcd214f0e47b12ad09bd6c07398eab3648d5d396f8669')
    version('2.3.4',  sha256='ec5f1a0aabe956f11c78b781ed4229300281ae35b1ecb104f8b4d83ae946d66b')
    version('2.3.3',  sha256='0ae1b1dc1ee870d307ae6ad4546778377b04055520d3771dab1290e60ab13286')
    version('2.3.2',  sha256='dbf0deb003531cbd2493986718a1b34a113c914238a90de8b5b3218217257d82')
    version('2.3.1',  sha256='628d4ea97a0709c6044d316979a1107c861518a17142d3bd7bf33b64fa351aef')
    version('2.3',    sha256='fcb20596c72fb5d713c3f0e11b613594628cde35c3ed083be7778fe92e453fd8')
    version('2.2.5',  sha256='58dc8df59aed1e4d9d50eef9e4c4c0789fa283b50f7a093932d0f467424484ee')
    version('2.2.4',  sha256='0959d3687d7e47c16c40808b1be704aa5a81355fb2944aff2ac7bf3abb998f7d')
    version('2.2.3',  sha256='3ac98293f4b82082c85e253011dd294c7ef03690b8a5b04b2b2e995437e5bd94')
    version('2.2.2',  sha256='46a544e8cba30cfd3d0ad0b8e59db95f77c0e459c54e5b98c71847547ddb3d65')
    version('2.2.1',  sha256='4b7827620d805375cccca9dca6142426d3dbce4a685267a72956a4383357ed25')
    version('2.2',    sha256='acb2a3a2845593b04c29d1809df8e9e3a7355b3b8256d0d146a88df1f569b6dd')
    version('2.1.3',  sha256='3c9f880747c0c23ea0cf69f40858f22344c2407c37e02aec4850e4154700456f')
    version('2.1.2',  sha256='e1d54354868d3beabba8245c29d16775875c165b0910c7a96f2bfd849b3f95ba')
    version('2.1.1',  sha256='c3c41d65fc490494084d7f4ddac81c259c26e1f64bf5428778410d701985b5d8')

    depends_on('bison', type='build')
    depends_on('texinfo', type='build')
    depends_on('gettext', type='build')

    # Untested whether glibc really does not build with newer compilers, or
    # whether it's just the configure scripts that complains.
    # Definitely for gcc 10 the configure script is just flawed, they didn't
    # expect multidigit major versions of gcc.
    conflicts('%gcc@10:', when='@:2.20')
    conflicts('%gcc@5:', when='@:2.15')
    conflicts('%gcc@3:', when='@:2.2')

    # Old versions require make 3.x; leaving this here as a comment.
    # depends_on('gmake', type='build')
    # conflicts('gmake@4:', when='@:2.18')

    # autotools deps
    depends_on('autoconf',  type='build', when='@master')
    depends_on('automake',  type='build', when='@master')
    depends_on('libtool',   type='build', when='@master')
    depends_on('m4',        type='build', when='@master')
