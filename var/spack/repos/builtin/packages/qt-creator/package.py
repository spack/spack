# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class QtCreator(QMakePackage):
    """The Qt Creator IDE."""
    homepage = 'https://www.qt.io/ide/'
    url      = 'http://download.qt.io/official_releases/qtcreator/4.8/4.8.0/qt-creator-opensource-src-4.8.0.tar.gz'

    list_url = 'http://download.qt.io/official_releases/qtcreator/'
    list_depth = 2

    version('4.14.0', sha256='6175e257c892f3c15a5a421fbc30bf4ae02b6c8f80d2663919fe0bf2278e5904')
    version('4.13.3', sha256='2f78f4c0a03c27fea4b9d85cb913fcb0c6ca8b2bd56ea6b2ee09db42dd60d4e1')
    version('4.13.2', sha256='73f3356be1a3cd21fcc9001bedd5cc7c54e76489c138b0748297591f3f61e5c9')
    version('4.13.1', sha256='f8f8fc84e6afe90eb60fe0f8e4bf16fdf5331ba44b996dc6fb4c1df20cf319a1')
    version('4.13.0', sha256='4002917702b70079f629c6969088eb7dadb9420b601408ba81c021d3e07c368e')
    version('4.12.4', sha256='26c484412bf3ac6ce6f97e1147fcdd29d7ddc396826acf6d4a90afd03610708b')
    version('4.12.3', sha256='262d3e9f0c5a8d0f85b568a9ebbcc38a46feedc8fdd9284c22b89548de19f9d3')
    version('4.12.2', sha256='965a46237311d884ac634f27de85b37956ef459535634ba9b5511235f6702c4f')
    version('4.12.1', sha256='4022738235c549808ef807bfdb8e96da6c44ce8c408c03be4a91b0395997f766')
    version('4.12.0', sha256='0f51de99574cdec9991faba8d32ecc269364dfd56e57065ebfc57e761118f920')
    version('4.11.2', sha256='a118632b8c53226b1030318471a7951582bf64aaa0bdf1faa79a6a11aa583d32')
    version('4.11.1', sha256='5a90b864632b94ecc38508c8743334a07ea4f5804fa971a7cf3a2fe844864578')
    version('4.11.0', sha256='d9b68eb900f7e1ab6b5bd050ffc9d7f01a91e1923b776edd017066d9f5b35205')
    version('4.10.2', sha256='86bfded5b11f7ff6edf84fbdc6b335a5d21bf545ab850b409c4a9762089ebb2a')
    version('4.10.1', sha256='7f07d7dfef503e8133ac95c6355dfe05c5bbaafdbf1bc7ba3d43634758d524b9')
    version('4.10.0', sha256='e3b7469abf50af55a6058aef16ee567f6355e78dd6e66fc56177c4d47dba5689')
    version('4.9.2',  sha256='914844191fc3a2fd58792cfd54aeffb80f0855bcbf6431b37ee3898879e6ab4a')
    version('4.9.1',  sha256='12d3e2963b83a82d1a7699211061032cd293d3672cac72b46d3e3ae492c98719')
    version('4.9.0',  sha256='e6401acf36a304739308d3958cf9abb1f43ef991d4b84f3642fb3875ef0e221a')
    version('4.8.2',  sha256='7353ece17b18d6584abc60430a077beb60db6f609fa5568c084ab7a460c0ed75')
    version('4.8.1',  sha256='849c5687b9447e5018afeb048a807f274b471619b71157aeef5fab037cfdbca2')
    version('4.8.0', sha256='4c4813454637141a45aa8f18be5733e4ba993335d95940aadf12fda66cf6f849')

    depends_on('qt@5.6.0:+opengl')
    # Qt Creator comes bundled with its own copy of sqlite. Qt has a build
    # dependency on Python, which has a dependency on sqlite. If Python is
    # built with a different version of sqlite than the bundled copy, it will
    # cause symbol conflict. Force Spack to build with the same version of
    # sqlite as the bundled copy.
    depends_on('sqlite@3.8.10.2', when='@:4.4.0')
    depends_on('sqlite@3.8.10.3:', when='@4.8.0:')

    # Qt Creator 4.3.0+ requires a C++14 compiler
    conflicts('%gcc@:4.8', when='@4.3.0:')

    def url_for_version(self, version):
        url = 'http://download.qt.io/official_releases/qtcreator/{0}/{1}/qt-creator-opensource-src-{1}.tar.gz'
        return url.format(version.up_to(2), version)

    def setup_build_environment(self, env):
        env.set('INSTALL_ROOT', self.prefix)

    def qmake_args(self):
        return ['-r']
