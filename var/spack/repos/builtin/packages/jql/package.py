# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jql(CargoPackage):
    """A JSON Query Language CLI tool built with Rust"""

    homepage = "https://github.com/yamafaktory/jql"
    crates_io = "jql"
    git = "https://github.com/yamafaktory/jql.git"

    # jql doesn't build with prefer_dynamic at present, so switch default to
    # False
    variant(
        'prefer_dynamic',
        default=False,
        description='Link Rust standard library dynamically'
    )

    version('master', branch='master')
    version('2.6.1', sha256='849810db82ae770c9e9c64ee5a739ef624b67cf5e37ae806ce62fccee0cb8220')
    version('2.6.0', sha256='31de69015bba9eb1d8357f9521e7d7e90ab2acb8ec523c16596396609a7d78b5')
    version('2.5.1', sha256='1c84ff188c6061383e211d9dddc76b082d2616e6d4ed52cd0d496ff975ffb46f')
    version('2.5.0', sha256='e762490c168f2876d6ed19c7bba5603934143adcc189b718cff860487ade78d4')
    version('2.4.9', sha256='2536ee235232a4d20237e55ad2d316c18004168c4a69d806f8b269e7e674254e')
    version('2.4.8', sha256='93d331d547410bb83525c9a381402b7ce5bc47ffa5eae0d13a1d87ae964c3d97')
    version('2.4.7', sha256='9e3b2d5e07308e26b69046d655c6645dd02b72f0c1f16191dea2b52a8363d0ac')
    version('2.4.6', sha256='fd796b1860dcb7a5312532bdd3a0183529d69ecbe8b9245a54eaeee56e98dfbd')
    version('2.4.5', sha256='f69f971951bd9a0908f8e6b902fdb1e0f91666dcc4c545a0d72f4ceede8c3386')
    version('2.4.4', sha256='a6b6bcc9277183676f8647f337c39476e33f894060c767ca35ba0c52b1e59186')
    version('2.4.3', sha256='6f671809ea5d8599175ea74257b8bb259794d891b19ca35f0ef5a7ea94b48ae8')
    version('2.4.2', sha256='1c96ff195b060662b5f379436fea0a8535b8098517241563e2d7d7401d01c24b')
    version('2.4.1', sha256='d7e576ef64e279bb89a6a7484547b4458ab75e5d65c9c16a2ddc20a4c1463cb5')
    version('2.4.0', sha256='97fc40e2c8955b49e99db550c24be7b771d01ac5c1acdb0a0222db73be223fc5')
    version('2.3.4', sha256='56d0bb7b032e7ede337682aeced54fee115838b86c7447f8bfc7135c1be3877e')
    version('2.3.3', sha256='95d7f6932edf26473152a70f07507b196deeddb917aabd7d2700706b60857f5f')
    version('2.3.2', sha256='86b90d15f074a7952d852f11e7cbb6a8d87a226476f3ea981023201715aeee12')
    version('2.3.1', sha256='bef989a74f3f1219bce0901753a0b899ec7567b2c98852b53231ec2fe0c6ee14')
    version('2.3.0', sha256='14252d54463efe0d7a335ca9c338b37f994f2f51c25a301089cc81bca13498d7')
    version('2.2.0', sha256='683b1deda3f8875d6aa9ad27d023aa5bdf3c5ac21ac896ffbd9ea1ea5e31d557')
    version('2.1.2', sha256='14eb9f997e31e22505d0b5add2ecab729f0c47e969884715bbe479205f654b25')
    version('2.1.1', sha256='d2a09550f029795b5969e5617c47337b0a630d35e1a23817a761d47836487760')
    version('2.1.0', sha256='1f2ec91abbe5250ffc55dc65c84392aff141b9e68fa915be74e1082f9d316d06')
    version('2.0.0', sha256='87f1f44acfc273bb5c25f42584951aabcf470f88222718416570f4a47c49b0d5')
    version('1.0.1', sha256='85ce5fc4aeb87b17d8aaaf56315930d592612c9d78b84fe4d74b09f373a32693')
    version('1.0.0', sha256='5ba71f66d55b535b490805af9acbc10acab0feaa475fa8ea17ca2c103ac7c6b3')
    version('0.2.2', sha256='1b6aebdf8fef72eaa169d97c0061d16c4090a6f269fe6363ff1bbc54b5a9d1c0')
    version('0.2.1', sha256='36b0a0410470b9f23c653fbf0e36649a1bab3fb7a1288968fc808d89662b0571')
    version('0.2.0', sha256='dc3b82009f9d8168470203b6116952755890802032bfcbc3826d8c0218f4c544')
    version('0.1.8', sha256='54935f2e65db2a92e61fe1691b6b685a932902cec91d728171ed762f25d015a2')
    version('0.1.7', sha256='22e890bc23c7755ddc94665536275414f6a73c261fab89bbcdc926c51cec7598')
    version('0.1.6', sha256='6c7202d2e10e17ad303dad1559808e76b9fedb55ba813252840a98f33910d9fd')
    version('0.1.5', sha256='b7879437de97c74125cf01d68d696b6ab27f0afcdfd3bbd59809b8af9c3acafa')
    version('0.1.4', sha256='eb0b75121200d1bf1988d6c0f151f3c090d8d5244c35dea477c9bca7f8c0faa2')
    version('0.1.3', sha256='82389f350f401f8cc71420f0b257965c1c87644ab8b529e64025628028280d5c')
    version('0.1.2', sha256='eba8d52ca0fdc81207e095d9a873815e3426376f0be7a97d4ab9e9a7733f2f33')
    version('0.1.1', sha256='d958a1bfa18c0d0e0e83cebe16336b67646921468e6ddac0757831497588bb57')
    version('0.1.0', sha256='43f0aa99f98ab4bf152e106d393e8dba2f1ca94276e0c73a0918ef35636a8471')
