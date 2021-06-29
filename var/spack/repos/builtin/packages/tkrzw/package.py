# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tkrzw(AutotoolsPackage):
    """Tkrzw is a C++ library implementing database managers with various algorithms."""

    homepage = "https://dbmx.net/tkrzw/"
    url      = "https://dbmx.net/tkrzw/pkg/tkrzw-0.9.22.tar.gz"
    git      = "https://github.com/estraier/tkrzw.git"

    version('master', branch='master')
    version('0.9.22', sha256='f892dcabc87d53086a7c1db129d05dda9c1e6b341d94d438daa8bf6a9e55407c')
    version('0.9.21', sha256='47211285fe41b5697d67eb4c22e850109acb4c657ebbaaf7eb815d3aac5bcc99')
    version('0.9.20', sha256='6750c8539a0c874c2ae673f852b47373f3d688365bd0ef97abb857b02a84095f')
    version('0.9.19', sha256='77c456368c0a0e241a87075bfe6f24a945fd603be5b5c63f6ae8af6f3aa87b3a')
    version('0.9.18', sha256='f1b4151aa932b413380290ab63117ff824006aef6812a6f854a5112969de52c8')
    version('0.9.17', sha256='aa2d40babf275a0b97d81706defaaa5c974724b3c8ffa028b9b46367fe151522')
    version('0.9.16', sha256='2380b3de12ffea78d59249fb3ac3a2b16a4422b3a3282d0afcf450286dc3622d')
    version('0.9.15', sha256='1e0e858c625804ae77c9386d5ded42c62211a356406d9264a4a37473d2f958cd')
    version('0.9.14', sha256='57671a539bb9c0a223e8117c83053aa43fa9050e9231ebef7c6411f65cdaeaa6')
    version('0.9.13', sha256='a6806fd30443cc2bed4539437bd8858b14a38fc81825fe4c49e754b7c133c866')
    version('0.9.12', sha256='6d45a28015012763e55e959a71e6a0a31f808f4f2867784c750f96e16aa50c8b')
    version('0.9.11', sha256='1d93a6966f9ab1f15568ee3d53ac54809f4b73230d0062b4ad65ebb6578f302e')
    version('0.9.10', sha256='6956a33d1ccfca1c290851dc74c625dd6a3c8dc246264c8d686ad89d58f58b25')
    version('0.9.9',  sha256='e16cd6b10ce4d97a59958a205ffce7b0db09f49f1b18c437a869fa0ae1279b81')
    version('0.9.8',  sha256='5ee485c12060963b49963242545eb28524f8917e27db02def220d35edbba4fa5')
    version('0.9.7',  sha256='90e0244b5b67d6142cbe3186564e39676d06024203c34a492b73b17561067a95')
    version('0.9.6',  sha256='6194d9fb4c9cb565e05d1fdd0569bd25ba26a987f037aeee226d35145a54d0c2')
    version('0.9.5',  sha256='02da0da3f43cc4932851b1b00174acd0835becfda966d5a9f874dc2205e1fb52')
    version('0.9.4',  sha256='727a52fc706ee28ef45a0fd6bce8c08911365dd016ccdb4cce7ad3a595b7c0ed')
    version('0.9.3',  sha256='945b978402425de6f4cb156544ddf34d928b28100ff93d931816eec3b51be9aa')
    version('0.9.2',  sha256='9040af148ab3f35c6f1d4c83f2eba8b68625dbd760f2c0537a9981dbc9bbc661')
    version('0.9.1',  sha256='1062502f93d4a9b387372d89265a9ede1704c6bcadd9aac23f5fc8383e26045a')

    conflicts('%gcc@:7.2.0')  # need C++17 standard
