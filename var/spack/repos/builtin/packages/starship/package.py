# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Starship(CargoPackage):
    """The minimal, blazing-fast, and infinitely customizable prompt for any
    shell!
    """

    homepage = "https://starship.rs/"
    crates_io = "starship"
    git = "https://github.com/starship/starship.git"

    # Change the defaults for prefer_dynamic and lto to reflect that starship
    # cannot build with prefer_dynamic at this time, and prefers to be built
    # with lto.
    variant(
        'prefer_dynamic',
        default=False,
        description='Link Rust standard library dynamically'
    )

    variant(
        'lto',
        default='fat',
        description='Link binaries with link-time optimization',
        values=('none', 'thin', 'fat')
    )

    depends_on('libgit2')

    def setup_build_environment(self, env):
        env.append_flags('LIBGIT2_SYS_USE_PKG_CONFIG', '1')

    version('master', branch='master')
    version('0.41.3', sha256='891dec63d2b8ffed3d2388c0449dbd939f6da1b26747ba0ed1a01e4d47f32fce')
    version('0.41.2', sha256='cf001ee42fa48e9f51a272796f8e773ef3f69eb799a288724a7a8252512df862')
    version('0.41.1', sha256='0f9adb5803700dc8b489e48bf30caef979b7ae4a55587af2e84c039e89692eee')
    version('0.41.0', sha256='fd80f0b4fa3961ff1e31452cf12c7b2ae9166566a200a0bd89cffd261fbcbaeb')
    version('0.40.1', sha256='9ef6088232e4ad958bdf63ff55ce93c6c1455acdc4ca92808126b7218c1fab18')
    version('0.40.0', sha256='5ab9c11cb41f17d60f9d6807d01152c009f5b76501f664074772df7e26b2759b')
    version('0.39.0', sha256='596bca871e5a61006c78fb59ca7a03ee822ab7d91f65af8e3d8492ece9ae7df1')
    version('0.38.1', sha256='98b0a42757834d8797244384623348dacc9af18b58c1e0e09ef4acd9ec393f40')
    version('0.38.0', sha256='43eedcc781b87f19ee276f6ce6057c7dcb3987b161bbb195cb1aaff0bceb26fc')
    version('0.37.1', sha256='3b7338a1617ab5c28f7b081fdd693832c5a9ce5b1f6f33b17bcde11b9b27d96f')
    version('0.37.0', sha256='588e250206eec64cee803f0d7c1d1f7c1d3ba7e123d513f0311b172d07a0f755')
    version('0.36.1', sha256='e105b4d5585c6f6382db46872747df88ca4800ccbd88fff77451431b49ec1052')
    version('0.36.0', sha256='7014395cd957c9fd812328538f41b2062918f471dd8aa1b011f19b7315aca868')
    version('0.35.1', sha256='5e9fd041a10d378370baa43669ccf11a8385a495d492ce57e5d144f83007a8ba')
    version('0.34.1', sha256='ed09f4d4c842bf92dd5c3f4f04a699b2790265f3c8836638df6bf3dfa236fb8d')
    version('0.33.1', sha256='91efa8a7ad3da400fa610a1f49f9aca455de4082913a48e2f3d6cad64813459d')
    version('0.33.0', sha256='b9b7bec21386cada82f09f68347ba58913469be2878488bb5f1220476ffb3e5a')
    version('0.32.2', sha256='06ecd4876210414b262fa501bfaa0b787a9025f3eb6e8dd883ca28306c67c4c3')
    version('0.32.1', sha256='54f59ac9299e6d78f4edca7cdf418428e9d108afa2d546e4a8231e1496e4f527')
    version('0.32.0', sha256='671aeb99169a10a84fce1ec0ae08db02e83998edd8441f436217245a324ddcda')
    version('0.31.0', sha256='b14b1b3b0776dad58506172e3978bb557dde7eeb2d3b7a2aa34e17e1e84e79a7')
    version('0.30.1', sha256='4c81211a8b24985cdf54eebda0e7647844f76801e96dc5e93703c962086e52a1')
    version('0.30.0', sha256='77c5c155344cde3057bf55a300f1d9b35c479bd0596e6f3e89949fb840a9f448')
    version('0.29.0', sha256='d638a18eb63bfb716bbcbf9802ca4016a93eb04b2bfa2bace33be2bfb91af109')
    version('0.28.0', sha256='0dd67e008b36f43c4dfb7663ead636e61a8db941be37459bf55a3c849aefacae')
    version('0.27.0', sha256='907328db2402a3a222b489f9842ec1b21df114b498a1220080986d810454f029')
    version('0.26.5', sha256='f894d024732efa305ffd2cfd20b770de9c2ba5128329d282c30d14d7c4a2f146')
    version('0.26.4', sha256='d31191331ef70afd5c8f88515850ce50ae4a7ad5a9d7d1046eba6ceb8e9707d8')
    version('0.26.3', sha256='dbb202f139822a71dfc63a33fb6360bf7412ec0f166952e1b84f396b80ae370c')
    version('0.26.2', sha256='3348541511eb3ce47d6bcdc0f40c55c21d199bae7cac79de952ad5167101f151')
    version('0.26.0', sha256='63b7637dec4c6ffb61876179c63d6c9e73c13b9703dc57ee07b31cd6341256aa')
    version('0.25.2', sha256='fbcd99721988315ab65bc60e398991bcb052b36efd37ee6297d52e545b12ee4d')
    version('0.25.1', sha256='a6e44b9c76812f858d5b8886c9f4617bb855121d7c0bc1f8c0cce84d65380393')
    version('0.25.0', sha256='4c628ebfbf6bc8c5549a8f097d46875b6e84f1d8b6481eaddfd2ecc85dc79ff0')
    version('0.24.0', sha256='b22be5eac207486cc8aec9afbc5ef9c9923ed4d715e9c06eedec0471dd0f8523')
    version('0.23.0', sha256='465dc85f7c2e1f738b3097ddf431cb26cd28f9f59156ed2e048a5d11cc5f83f0')
    version('0.22.0', sha256='43070194dc4cd97f37367c50ca51420c3b86303d4b259a9a73db71ee1658028d')
    version('0.21.0', sha256='623fe474026c898d94e98ab4f37212a710e3365eedfa6e99bf520ad20bc3e160')
    version('0.20.2', sha256='6ba4819b8f49d2cead199aedbdd21d799d7fcf7845c2976bbe560b880412d268')
    version('0.20.1', sha256='8937bd5bace8cede777754185e15c9a74eb07e9f7dcff2e935f3697c0415522d')
    version('0.19.0', sha256='61477a846487877c5a135d49cb6675bcab09ac1b30536db040af0526c04bf88b')
    version('0.18.0', sha256='6a6650d68f4b4e5b89a84631a97dc3f20b9d03abdf5fde10a6109a5348f1f501')
    version('0.17.0', sha256='4381c1da2761d3f047aa6be54449286371c7059a1a1759dbeb4952edda2bd3f2')
    version('0.16.0', sha256='5d56640b5284ea654e8201a352f68180117e8c825ddb5d76cdfac1121ec39fa7')
    version('0.15.0', sha256='36987e3c2f763c81111693212ef828ba8bce2980e91af1544c8b74fa5933b5ee')
    version('0.14.1', sha256='a6055b80f0a36f1c0ec9a258a9df1291037c3643ab392aa9c7dc82eb9d306610')
    version('0.14.0', sha256='dc78f8115d8acbb595a555fb15223f1fd80c3e5148867b75a3a3b7747b4649ae')
    version('0.13.1', sha256='6b0abd488652e7eb3c208f791c2cc81dcc051fc3b46ba1c6cb6ba2cd7d0e599a')
    version('0.13.0', sha256='bd2b315763477d8aa374b21a30df492109653692d724345ca0dd210d1e869cc2')
    version('0.12.2', sha256='cb81f2d59323e9f49e5f3efbe2d1376bc6fe4cada2ad4b0df46efb1e55df772f')
    version('0.12.1', sha256='dcbab92eb9c67885400cdb5380089277db8194559e2c0bc4620df1338e312e66')
    version('0.12.0', sha256='ed60a46c5bad275ab63e109a2d3323677b23600fe10ada2f5d360b9beb9f6e90')
    version('0.11.0', sha256='209ec8a533b1a872849c5ecb5c13d732227b586649222ee1d11957f19f0843a9')
    version('0.10.1', sha256='718da27156409c195b34469f7c24dff2b040f22231a6ee79baab09be3de35f82')
    version('0.10.0', sha256='c4239d656d5333ea1d2009c794662c3adcb528a885e1d23075887c2c31386ed4')
    version('0.9.1',  sha256='baf18ffbea76f73ad34c34b18c327591d5b0b1626adb5f2001df69fa5998b0d9')
    version('0.9.0',  sha256='692b71c1bdcf1b6481c85b0562b53ce2bba791e3bbc52a22dfe58f79a26fefca')
    version('0.8.7',  sha256='5236a89cd6f55fc833ff19b913e4549b40bd689bf22e13670e4dca8182be75a2')
    version('0.8.6',  sha256='e1a07615956fd7e5c5b39a303293dfb3877ec2704b69ca197bb3d8e22d5ada47')
    version('0.8.5',  sha256='d962e8eeeeee2c14407cb04f7bb902774f8ac7df92b40eeef637dd019c23542b')
    version('0.8.4',  sha256='e49bc39d71eb2f3bedb5944be367fa954ab1fab088cdb5d6a9d036fda3833cea')
    version('0.8.3',  sha256='c045e91529759f1e42995c9e99d4f66f941b51e0a7fd137ee7d48226ec66b764')
    version('0.8.2',  sha256='1327f51762d027891bc8137552ca4aa1efc72f1b8f2a9e194ad416f718cbb5c5')
    version('0.8.1',  sha256='b2c414efda8195f3fd347323ff6f94c05a24b06c0b60fff46b7699d8d7d4f7b7')
    version('0.8.0',  sha256='575aae2068a782890870cb5b849fb4e56e6ec2d7c0d22744b396df449f513b9f')
    version('0.7.0',  sha256='7fd8f953107d75bc8be8484e466293b2946c5c7590d511bb52787f36b91de618')
    version('0.6.0',  sha256='db06781c363e3702665a8d77d360a19921befef49f6c134dfbbc6e0ed645fc31')
    version('0.5.0',  sha256='9df9285748b78354f49a4ae73104860193434c400d54553b0fc110919b0e744f')
    version('0.4.1',  sha256='00beece3c96c60b3356e90dd7b92095997a61041e3721ba96e980cd12a569802')
    version('0.4.0',  sha256='0ecdb572ee5e3397acbe0ebd8205dba0248b9dc4fd4cf281ed2da10128bfd110')
    version('0.3.2',  sha256='7244fe099712af03d51e515d07768c61507de23664a4d38f29ffc4437babeba1')
    version('0.3.1',  sha256='35d5c957de60ae3160ad2128e415580631fd67560d33750ab662750f0736df1a')
    version('0.3.0',  sha256='8c3b50b1c73e5e3ebfc99f884c9c3ae9b8f52d266358251a8b27da76734ffe53')
    version('0.2.0',  sha256='04dd95848bbaab2d06811777aa0de2d5676e8f05ad468952ea9e99415bdd4963')
