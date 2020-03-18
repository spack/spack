# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from six import iteritems

class Rust(Package):
    """The Rust programming language toolchain
    
    This package can bootstrap any version of the Rust compiler. It does this
    by downloading the platform-appropriate binary distribution of the desired
    version of the rust compiler, and then building that compiler from source.

    Rust has a few build and link time dependencies. The big one is LLVM. This
    package's default is to use Rust's vendored version of LLVM as it contains
    a number of customizations just for Rust. However, an external or
    spack-built LLVM can be used if you're you're a power user by setting the
    `llvm` variant.
    """

    homepage = "https://www.rust-lang.org"
    url = "https://static.rust-lang.org/dist/rustc-1.42.0-src.tar.gz"

    maintainers = ["AndrewGaspar"]

    phases = ['configure', 'build', 'install']

    extendable = True

    variant(
        'rustfmt',
        default=True,
        description='Formatting tool for Rust code'
    )

    variant(
        'analysis',
        default=True,
        description='Outputs code analysis that can be consumed by other tools'
    )

    variant(
        'clippy',
        default=True,
        description='Linting tool for Rust'
    )

    variant(
        'rls',
        default=False,
        description='The Rust Language Server can be used for IDE integration'
    )

    variant(
        'src',
        default=True,
        description='Install Rust source files'
    )

    variant(
        'llvm',
        default='vendored',
        description='LLVM distribution to use. "external" is at your own risk',
        values=('vendored', 'external'),
        multi=False
    )

    depends_on('cmake', type='build')
    # We don't use binutils on Mac - we pick up ar either from the system or
    # compiler
    depends_on('binutils', type='build', when='platform=linux')
    depends_on('binutils', type='build', when='platform=cray')
    depends_on('python@:2.8', type='build')
    depends_on('openssl')
    depends_on('libssh2')
    depends_on('libgit2')

    version('1.42.0', sha256='d2e8f931d16a0539faaaacd801e0d92c58df190269014b2360c6ab2a90ee3475')
    version('1.41.1', sha256='38c93d016e6d3e083aa15e8f65511d3b4983072c0218a529f5ee94dd1de84573')
    version('1.41.0', sha256='5546822c09944c4d847968e9b7b3d0e299f143f307c00fa40e84a99fabf8d74b')
    version('1.40.0', sha256='dd97005578defc10a482bff3e4e728350d2099c60ffcf1f5e189540c39a549ad')
    version('1.39.0', sha256='b4a1f6b6a93931f270691aba4fc85eee032fecda973e6b9c774cd06857609357')
    version('1.38.0', sha256='644263ca7c7106f8ee8fcde6bb16910d246b30668a74be20b8c7e0e9f4a52d80')
    version('1.37.0', sha256='120e7020d065499cc6b28759ff04153bfdc2ac9b5adeb252331a4eb87cbe38c3')
    version('1.36.0', sha256='04c4e4d7213d036d6aaed392841496d272146312c0290f728b7400fccd15bb1b')
    version('1.35.0', sha256='5a4d637a716bac18d085f44dd87ef48b32195f71b967d872d80280b38cff712d')
    version('1.34.2', sha256='c69a4a85a1c464368597df8878cb9e1121aae93e215616d45ad7d23af3052f56')
    version('1.34.1', sha256='b0c785264d17e1dac4598627c248a2d5e07dd39b6666d1881fcfc8e2cf4c40a7')
    version('1.34.0', sha256='7ac85acffd79dd3a7c44305d9eaabd1f1e7116e2e6e11e770e4bf5f92c0f1f59')
    version('1.33.0', sha256='5a01a8d7e65126f6079042831385e77485fa5c014bf217e9f3e4aff36a485d94')
    version('1.32.0', sha256='4c594c7712a0e7e8eae6526c464bf6ea1d82f77b4f61717c3fc28fb27ba2224a')
    version('1.31.1', sha256='91d2fc22f08d986adab7a54eb3a6a9b99e490f677d2d092e5b9e4e069c23686a')
    version('1.30.1', sha256='36a38902dbd9a3e1240d46ab0f2ca40d2fd07c2ab6508ed7970c6c4c036b5b29')
    version('1.30.0', sha256='cd0ba83fcca55b64c0c9f23130fe731dfc1882b73ae21bef96be8f2362c108ee')
    version('1.29.2', sha256='5088e796aa2e47478cdf41e7243fc5443fafab0a7c70a11423e57c80c04167c9')
    version('1.29.1', sha256='f1b0728b66ce6bce6d72bbe5ea9e3a24ea22a045665da2ed8fcdfad14f61a349')
    version('1.29.0', sha256='a4eb34ffd47f76afe2abd813f398512d5a19ef00989d37306217c9c9ec2f61e9')
    version('1.28.0', sha256='1d5a81729c6f23a0a23b584dd249e35abe9c6f7569cee967cc42b1758ecd6486')
    version('1.27.2', sha256='9a818c50cdb7880abeaa68b3d97792711e6c64c1cdfb6efdc23f75b8ced0e15d')
    version('1.27.1', sha256='2133beb01ddc3aa09eebc769dd884533c6cfb08ce684f042497e097068d733d1')
    version('1.27.0', sha256='2cb9803f690349c9fd429564d909ddd4676c68dc48b670b8ddf797c2613e2d21')
    version('1.26.2', sha256='fb9ecf304488c9b56600ab20cfd1937482057f7e5db7899fddb86e0774548700')
    version('1.26.1', sha256='70a7961bd8ec43b2c01e9896e90b0a06804a7fbe0a5c05acc7fd6fed19500df0')
    version('1.26.0', sha256='4fb09bc4e233b71dcbe08a37a3f38cabc32219745ec6a628b18a55a1232281dd')
    version('1.25.0', sha256='eef63a0aeea5147930a366aee78cbde248bb6e5c6868801bdf34849152965d2d')
    version('1.24.1', sha256='3ea53d45e8d2e9a41afb3340cf54b9745f845b552d802d607707cf04450761ef')
    version('1.24.0', sha256='bb8276f6044e877e447f29f566e4bbf820fa51fea2f912d59b73233ffd95639f')
    version('1.23.0', sha256='7464953871dcfdfa8afcc536916a686dd156a83339d8ec4d5cb4eb2fe146cb91')
    version('1.22.1', sha256='8b7a42bdd6eb205a8c533eb41b5c42389a88158d060aed1e0f461f68c1fd3fd3')
    version('1.22.0', sha256='0ac96fbc4fc4a616f8b0ad2f458f2af7e03c141271624cfb2be907b05cbe4a69')
    version('1.21.0', sha256='1707c142244b5bd909993559c6116c81987c1de21d6207c05d3ecbe5bba548fa')
    version('1.20.0', sha256='2aa4875ff4472c6e35262bbb9052cb2623da3dae6084a858cc59d36f33f18214')
    version('1.19.0', sha256='15231f5053fb72ad82be91f5abfd6aa60cb7898c5089e4f1ac5910a731090c51')
    version('1.18.0', sha256='d2dc36e99b9e2269488b2bcddde43c234e6bde03edf70cba82a027ff49c36111')
    version('1.17.0', sha256='4baba3895b75f2492df6ce5a28a916307ecd1c088dc1fd02dbfa8a8e86174f87')
    version('1.16.0', sha256='f966b31eb1cd9bd2df817c391a338eeb5b9253ae0a19bf8a11960c560f96e8b4')
    version('1.15.1', sha256='2e7daad418a830b45b977cd7ecf181b65f30f73df63ff36e124ea5fe5d1af327')
    version('1.15.0', sha256='f655e4fac9c2abb93eb579e29c408e46052c0e74b7655cd222c63c6743457673')
    version('1.14.0', sha256='c790edd2e915bd01bea46122af2942108479a2fda9a6f76d1094add520ac3b6b')
    version('1.13.0', sha256='ecb84775ca977a5efec14d0cad19621a155bfcbbf46e8050d18721bb1e3e5084')
    version('1.12.1', sha256='97913ae4cb255618aaacd1a534b11f343634b040b32656250d09d8d9ec02d3dc')
    version('1.12.0', sha256='ac5907d6fa96c19bd5901d8d99383fb8755127571ead3d4070cce9c1fb5f337a')
    version('1.11.0', sha256='3685034a78e70637bdfa3117619f759f2481002fd9abbc78cc0f737c9974de6a')
    version('1.10.0', sha256='a4015aacf4f6d8a8239253c4da46e7abaa8584f8214d1828d2ff0a8f56176869')
    version('1.9.0',  sha256='b19b21193d7d36039debeaaa1f61cbf98787e0ce94bd85c5cbe2a59462d7cfcd')
    version('1.8.0',  sha256='af4466147e8d4db4de2a46e07494d2dc2d96313c5b37da34237f511c905f7449')
    version('1.7.0',  sha256='6df96059d87b718676d9cd879672e4e22418b6093396b4ccb5b5b66df37bf13a')
    version('1.6.0',  sha256='3002a4a00004b0727709abeefe1ab1b2731845e4dab74566f363861801bb3326')
    version('1.5.0',  sha256='641037af7b7b6cad0b231cc20671f8a314fbf2f40fc0901d0b877c39fc8da5a0')
    version('1.4.0',  sha256='1c0dfdce5c85d8098fcebb9adf1493847ab40c1dfaa8cc997af09b2ef0aa8211')
    version('1.3.0',  sha256='ea02d7bc9e7de5b8be3fe6b37ea9b2bd823f9a532c8e4c47d02f37f24ffa3126')
    version('1.2.0',  sha256='ea6eb983daf2a073df57186a58f0d4ce0e85c711bec13c627a8c85d51b6a6d78')
    version('1.1.0',  sha256='cb09f443b37ec1b81fe73c04eb413f9f656859cf7d00bc5088008cbc2a63fa8a')
    version('1.0.0',  sha256='c304cbd4f7b25d116b73c249f66bdb5c9da8645855ce195a41bda5077b995eba')
    

    rust_releases = {
        'x86_64-unknown-linux-gnu': {
            '1.42.0': '7d1e07ad9c8a33d8d039def7c0a131c5917aa3ea0af3d0cc399c6faf7b789052',
            '1.41.1': 'a6d5a3b3f574aafc8f787fea37aad9fb8a7946b383ae5348146927192ff0bef0',
            '1.41.0': '343ba8ef7397eab7b3bb2382e5e4cb08835a87bff5c8074382c0b6930a41948b',
            '1.40.0': 'fc91f8b4bd18314e83a617f2389189fc7959146b7177b773370d62592d4b07d0',
            '1.39.0': 'b10a73e5ba90034fe51f0f02cb78f297ed3880deb7d3738aa09dc5a4d9704a25',
            '1.38.0': 'adda26b3f0609dbfbdc2019da4a20101879b9db2134fae322a4e863a069ec221',
            '1.37.0': 'cb573229bfd32928177c3835fdeb62d52da64806b844bc1095c6225b0665a1cb',
            '1.36.0': '15e592ec52f14a0586dcebc87a957e472c4544e07359314f6354e2b8bd284c55',
            '1.35.0': 'cf600e2273644d8629ed57559c70ca8db4023fd0156346facca9ab3ad3e8f86c',
            '1.34.2': '2bf6622d980a52832bae141304e96f317c8a1ccd2dfd69a134a14033e6e43c0f',
            '1.34.1': '8e2eead11bd5bf61409e29018d007c6fc874bcda2ff54db3d04d1691e779c14e',
            '1.34.0': '170647ed41b497dc937a6b2556700210bc4be187b1735029ef9ccf52e2cb5ab8',
            '1.33.0': '6623168b9ee9de79deb0d9274c577d741ea92003768660aca184e04fe774393f',
            '1.32.0': 'e024698320d76b74daf0e6e71be3681a1e7923122e3ebd03673fcac3ecc23810',
            '1.31.1': 'a64685535d0c457f49a8712a096a5c21564cd66fd2f7da739487f028192ebe3c',
            '1.30.1': 'a01a493ed8946fc1c15f63e74fc53299b26ebf705938b4d04a388a746dfdbf9e',
            '1.30.0': 'f620e3125cc505c842150bd873c0603432b6cee984cdae8b226cf92c8aa1a80f',
            '1.29.2': 'e9809825c546969a9609ff94b2793c9107d7d9bed67d557ed9969e673137e8d8',
            '1.29.1': 'b36998aea6d58525f25d89f1813b6bfd4cad6ff467e27bd11e761a20dde43745',
            '1.29.0': '09f99986c17b1b6b1bfbc9dd8785e0e4693007c5feb67915395d115c1a3aea9d',
            '1.28.0': '2a1390340db1d24a9498036884e6b2748e9b4b057fc5219694e298bdaa37b810',
            '1.27.2': '5028a18e913ef3eb53e8d8119d2cc0594442725e055a9361012f8e26f754f2bf',
            '1.27.1': '435778a837af764da2a7a7fb4d386b7b78516c7dfc732d892858e9a8a539989b',
            '1.27.0': '235ad78e220b10a2d0267aea1e2c0f19ef5eaaff53ad6ff8b12c1d4370dec9a3',
            '1.26.2': 'd2b4fb0c544874a73c463993bde122f031c34897bb1eeb653d2ba2b336db83e6',
            '1.26.1': 'b7e964bace1286696d511c287b945f3ece476ba77a231f0c31f1867dfa5080e0',
            '1.26.0': '13691d7782577fc9f110924b26603ade1990de0b691a3ce2dc324b4a72a64a68',
            '1.25.0': '06fb45fb871330a2d1b32a27badfe9085847fe824c189ddc5204acbe27664f5e',
            '1.24.1': '4567e7f6e5e0be96e9a5a7f5149b5452828ab6a386099caca7931544f45d5327',
            '1.24.0': '336cf7af6c857cdaa110e1425719fa3a1652351098dc73f156e5bf02ed86443c',
            '1.23.0': '9a34b23a82d7f3c91637e10ceefb424539dcfa327c2dcd292ff10c047b1fdc7e',
            '1.22.1': '8cf4e840041fb05721673836997c5aac5673f733660927dfb64b8d653a3a94fa',
            '1.22.0': '11118f670343f3ebdd4790f845fd68f38db65b19261b81b3ab580d8425d0a7c6',
            '1.21.0': 'b41e70e018402bc04d02fde82f91bea24428e6be432f0df12ac400cfb03108e8',
            '1.20.0': 'ca1cf3aed73ff03d065a7d3e57ecca92228d35dc36d9274a6597441319f18eb8',
            '1.19.0': '30ff67884464d32f6bbbde4387e7557db98868e87fb2afbb77c9b7716e3bff09',
            '1.18.0': 'abdc9f37870c979dd241ba8c7c06d8bb99696292c462ed852c0af7f988bb5887',
            '1.17.0': 'bbb0e249a7a3e8143b569706c7d2e7e5f51932c753b7fd26c58ccd2015b02c6b',
            '1.16.0': '48621912c242753ba37cad5145df375eeba41c81079df46f93ffb4896542e8fd',
            '1.15.1': 'b1e7c818a3cc8b010932f0efc1cf0ede7471958310f808d543b6e32d2ec748e7',
            '1.15.0': '576fcced49744af5ea438afc4411395530426b0a3d4839c5205f646f15850663',
            '1.14.0': 'c71325cfea1b6f0bdc5189fa4c50ff96f828096ff3f7b5056367f9685d6a4d04',
            '1.13.0': '95f4c372b1b81ac1038161e87e932dd7ab875d25c167a861c3949b0f6a65516d',
            '1.12.1': '9e546aec13e389429ba2d86c8f4e67eba5af146c979e4faa16ffb40ddaf9984c',
            '1.12.0': '3a9647123f1f056571d6603e40f21a96162702e1ae4725ee8c2bc9452a87cf5d',
            '1.11.0': 'f4ebbd6d9494cb8fa6c410cb58954e1913546c2bca8963faebc424591547d83f',
            '1.10.0': 'f189303d52b37c8bb694b9d9739ae73ffa926cbdeffde1d5d6a5c6e811940293',
            '1.9.0':  '288ff13efa2577e81c77fc2cb6e2b49b1ed0ceab51b4fa12f7efb87039ac49b7',
            '1.8.0':  'd5a7c10070f8053defe07d1704762c91e94fc30a1020d16b111d63e9af365d48',
            '1.7.0':  'd36634bd8df3d7565487b70af03dfda1c43c635cd6f2993f47cd61fda00d890a',
            '1.6.0':  '8630cc02432b4423d64eeae4ef071ec58e5dd1f3d555a3a3cc34b759202813f6',
            '1.5.0':  '60b83f74d882ce2ba5bc979b5b0589dca56659f215b3259e7188fed8c50aac9d',
            '1.4.0':  '2de2424b50ca2ab3a67c495b6af03c720801a2928ad30884438ad0f5436ac51d',
            '1.3.0':  'fa755b6331ff7554e6e8545ee20af7897b0adc65f471dd24ae8a467a944755b4',
            '1.2.0':  '2311420052e06b3e698ce892924ec40890a8ff0499902e7fc5350733187a1531',
            '1.1.0':  '5a8b1c4bb254a698a69cd05734909a3933567be6996422ff53f947fd115372e6',
            '1.0.0':  'aab0d853314675d5e80e427c613a0e646ae75fbbc856b886dab682280f825d53'
        },
        'powerpc64le-unknown-linux-gnu': {
            '1.42.0': '805b08fa1e0aad4d706301ca1f13e2d80810d385cece2c15070360b3c4bd6e4a',
            '1.41.1': 'f9b53ca636625b3a2dd87600b6274223c11f866c9b5a34b638ea0013186659d3',
            '1.41.0': 'ba231b0d8273d6928f61e2be3456e816a1de8050135e20c0623dc7a6ea03ba68',
            '1.40.0': 'b1a23e35c383f99e647df6a9239b1dc9313e293deb70a76ba58e8ebe55ef623b',
            '1.39.0': '53b3fd942c52709f7e6fe11ea572d086e315a57a40b84b9b3290ac0ec8c7c84a',
            '1.38.0': 'f9ed1bb6525abdd4dd6ef10782ad45d2f71496e0c3c88e806b510c81a91c4ff7',
            '1.37.0': '27c59ec40e9e9f71490dc00bf165156ae3ea77c20ffa4b5e5fd712e67527b477',
            '1.36.0': '654a7a18d881811c09f630b0c917825b586e94a6142eceaede6b8046718e4054',
            '1.35.0': 'a933955adec386d75d126e78df5b9941936e156acb3353fc44b85995a81c7bb2',
            '1.34.2': '4ddd55014bbd954b3499859bfa3146bff471de21c1d73fc6e7cccde290fc1918',
            '1.34.1': '94ac92d08afcfa2d77ae207e91b57c00cb48ff7ba08a27ed3deb2493f33e8fb1',
            '1.34.0': '3027e87802e161cce6f3a23d961f6d73b9ed6e829b2cd7af5dfccf6e1207e552',
            '1.33.0': 'db885aa4c2c6896c85257be2ade5c9edea660ca6878970683e8d5796618329b5',
            '1.32.0': 'd6d5c9154f4459465d68ebd4fa1e17bad4b6cfe219667dddd9123c3bfb5dd839',
            '1.31.1': 'a6f61b7a8a06a2b0a785391cc3e6bb8004aa72095eea80db1561039f5bb3e975',
            '1.30.1': 'a7d4806e6702bdbad5017eeddc62f7ff7eb2438b1b9c39cbc90c2b1207f8e65f',
            '1.30.0': '0b53e257dc3d9f3d75cd97be569d3bf456d2c0af57ed0bd5e7a437227d8f465a',
            '1.29.2': '344003b808c20424c4699c9452bd37cdee23857dd4aa125e67d1d6e4bc992091',
            '1.29.1': '26a6d652ade6b6a96e6af18e846701ee28f912233372dfe15432139252f88958',
            '1.29.0': 'd6954f1da53f7b3618fba3284330d99b6142bb25d9febba6dbfedad59ca53329',
            '1.28.0': '255818156ec1f795ed808a44b4fdb8019187d5ebb7f837ae8f55a1ca40862bb6',
            '1.27.2': '11034d150e811d4903b09fd42f0cb76d467a6365a158101493405fff1054572f',
            '1.27.1': 'a08e6b6fed3329fcd1220b2ee4cd7a311d99121cf780fb6e1c6353bfeddfb176',
            '1.27.0': '847774a751e848568215739d384e3baf4d6ec37d27fb3add7a8789208c213aff',
            '1.26.2': 'ea045869074ae3617eeb51207ce183e6915784b9ed615ecb92ce082ddb86ec1f',
            '1.26.1': 'ad8b2f6dd8c5cca1251d65b75ed2120aae3c5375d2c8ed690259cf4a652d7d3c',
            '1.26.0': '3ba3a4905730ec01007ca1096d9fc3780f4e81f71139a619e1f526244301b7f4',
            '1.25.0': '79eeb2a7fafa2e0f65f29a1dc360df69daa725347e4b6a533684f1c07308cc6e',
            '1.24.1': '6f6c4bebbd7d6dc9989bf372c512dea55af8f56a1a0cfe97784667f0ac5430ee',
            '1.24.0': '25d9b965a63ad2f345897028094d4c7eafa432237b478754ccbcc299f80629c8',
            '1.23.0': '60f1a1cc182c516de08c1f42ada01604a3d94383e9dded6b237ae2233999437b',
            '1.22.1': 'b0c5149c16ce705c572b4c0976dd5c197309f12dda313f83a10e4f0a979eea6c',
            '1.22.0': '1fb64fc8f76ca8ae00fcc57774f1fb2e3517b46000f44cd7e50246ed90ecb976',
            '1.21.0': '67d4a1c5ed3c19168ca5fee799fc6a153a9b45d88e4351723fc41f409f87bec9',
            '1.20.0': 'cf5be95e2f8212b5231b175d2d2572fdf55a637997655eef460fdeec2ed6d349',
            '1.19.0': '9ca374e9ea1e5f33394d2a8278591def523cbf05ec0ecfa966673f10b72c035c',
            '1.18.0': '62cae76530faccf51ac8f92c1e65a9c3823465088bf4e6fdf0ece4197e74f5a3',
            '1.17.0': '2dda1fff20aecd7b208babfd45f70c608978fe2594916d1448e42757bb7e759f',
            '1.16.0': '4a6fcf1f6a015b9809e2fa7d3b35d117364e95df21a890089c8f5c06e252b7a5',
            '1.15.1': '3f40285145ad3b7cde703b18ac9c57bafb482c636da26d65f54abbf369b013cb',
            '1.15.0': 'b3d50b34d464ee1adb56b7924499eb619153fd486ea07a3400067725d119a0c5',
            '1.14.0': 'd3956c671b35fb43e6ebd1757719f862d7c700c223b65fa61bdf628ced81b3af'
        },
        'x86_64-apple-darwin': {
            '1.42.0': 'db1055c46e0d54b99da05e88c71fea21b3897e74a4f5ff9390e934f3f050c0a8',
            '1.41.1': '16615288cf74239783de1b435d329f3d56ed13803c7c10cd4b207d7c8ffa8f67',
            '1.41.0': 'b6504003ab70b11f278e0243a43ba9d6bf75e8ad6819b4058a2b6e3991cc8d7a',
            '1.40.0': '749ca5e0b94550369cc998416b8854c13157f5d11d35e9b3276064b6766bcb83',
            '1.39.0': '3736d49c5e9592844e1a5d5452883aeaf8f1e25d671c1bc8f01e81c1766603b5',
            '1.38.0': 'bd301b78ddcd5d4553962b115e1dca5436dd3755ed323f86f4485769286a8a5a',
            '1.37.0': 'b2310c97ffb964f253c4088c8d29865f876a49da2a45305493af5b5c7a3ca73d',
            '1.36.0': '91f151ec7e24f5b0645948d439fc25172ec4012f0584dd16c3fb1acb709aa325',
            '1.35.0': 'ac14b1c7dc330dcb53d8641d74ebf9b32aa8b03b9d650bcb9258030d8b10dbd6',
            '1.34.2': '6fdd4bf7fe26dded0cd57b41ab5f0500a5a99b7bc770523a425e9e34f63d0fd8',
            '1.34.1': 'f4e46b9994ccfab4a84059298d1dc8fd446b1bbb7449462e0459948f7debea0e',
            '1.34.0': 'e6bea8d865cc7341c17fa3b8f25f7989e6b04f53e9da24878addc524f3a32664',
            '1.33.0': '864e7c074a0b88e38883c87c169513d072300bb52e1d320a067bd34cf14f66bd',
            '1.32.0': 'f0dfba507192f9b5c330b5984ba71d57d434475f3d62bd44a39201e36fa76304',
            '1.31.1': '8398b1b303bdf0e7605d08b87070a514a4f588797c6fb3593718cb9cec233ad6',
            '1.30.1': '3ba1704a7defe3d9a6f0c1f68792c084da83bcba85e936d597bac0c019914b94',
            '1.30.0': '07008d90932712282bc599f1e9a226e97879c758dc1f935e6e2675e45694cc1b',
            '1.29.2': '63f54e3013406b39fcb5b84bcf5e8ce85860d0b97a1e156700e467bf5fb5d5f2',
            '1.29.1': '07b07fbd6fab2390e19550beb8008745a8626cc5e97b72dc659061c1c3b3d008',
            '1.29.0': '28a0473637585742f6d80ccd8afd88b6b400e65d623c33cb892412759444da93',
            '1.28.0': '5d7a70ed4701fe9410041c1eea025c95cad97e5b3d8acc46426f9ac4f9f02393',
            '1.27.2': '30c5cc58759caa4efdf2ea7d8438633139c98bee3408beb29ceb26985f3f5f70',
            '1.27.1': '475be237962d6aef1038a2faada26fda1e0eaea5d71d6950229a027a9c2bfe08',
            '1.27.0': 'a1d48190992e01aac1a181bce490c80cb2c1421724b4ff0e2fb7e224a958ce0f',
            '1.26.2': 'f193705d4c0572a358670dbacbf0ffadcd04b3989728b442f4680fa1e065fa72',
            '1.26.1': 'ebf898b9fa7e2aafc53682a41f18af5ca6660ebe82dd78f28cd9799fe4dc189a',
            '1.26.0': '38708803c3096b8f101d1919ee2d7e723b0adf1bc1bb986b060973b57d8c7c28',
            '1.25.0': 'fcd0302b15e857ba4a80873360cf5453275973c64fa82e33bfbed02d88d0ad17',
            '1.24.1': '9d4aacdb5849977ea619d399903c9378163bd9c76ea11dac5ef6eca27849f501',
            '1.24.0': '1aecba7cab4bc1a9e0e931c04aa00849e930b567d243da7b676ede8f527a2992',
            '1.23.0': '9274e977322bb4b153f092255ac9bd85041142c73eaabf900cb2ef3d3abb2eba',
            '1.22.1': 'c7cf38a9fe56cc03b61213899e0e2db2153ce4c69ed36b794264c5d3629dae57',
            '1.22.0': 'dcd0693666dbf595212323a2ee7c14bbe4ff94b527742a378be0482753ff99f2',
            '1.21.0': '75a7f4bd7c72948030bb9e421df27e8a650dea826fb5b836cf59d23d6f985a0d',
            '1.20.0': 'fa1fb8896d5e327cbe6deeb50e6e9a3346de629f2e6bcbd8c10f19f3e2ed67d5',
            '1.19.0': '5c668fb60a3ba3e97dc2cb8967fc4bb9422b629155284dcb89f94d116bb17820',
            '1.18.0': '30f210e3133121812d74995a2831cfb3fe79c271b3cb1721815943bd4f7eb297',
            '1.17.0': '1689060c07ec727e9756f19c9373045668471ab56fd8f53e92701150bbe2032b',
            '1.16.0': '2d08259ee038d3a2c77a93f1a31fc59e7a1d6d1bbfcba3dba3c8213b2e5d1926',
            '1.15.1': '38606e464b31a778ffa7d25d490a9ac53b472102bad8445b52e125f63726ac64',
            '1.15.0': '8b02c3714d30a6111af805d76df0de28c045f883a9171839ebd5667327f2e50a',
            '1.14.0': '3381341524b0184da5ed2cdcddc2a25e2e335e87f1cf676f64d98ee5e6479f20',
            '1.13.0': 'f538ca5732b844cf7f00fc4aaaf200a49a845b58b4ec8aef38da0b00e2cf6efe',
            '1.12.1': '0ac5e58dba3d24bf09dcc90eaac02d2df053122b0def945ec4cfe36ac6d4d011',
            '1.12.0': '608c4530dcbd2e29c9600a0743b1a83a62556c9525385a7e1a7ba4aa1467a132',
            '1.11.0': '2cdbc47438dc86ecaf35298317b77d735956eb160862e3f6d0fda0da656ecc35',
            '1.10.0': '4bb71249f4afd7cee07f63d681f9fcb1b525ee3dfd49722adab7a40024e45af7',
            '1.9.0':  'd59b5509e69c1cace20a57072e3b3ecefdbfd8c7e95657b0ff2ac10aa1dfebe6',
            '1.8.0':  '606bfa2ac277f2f37be1bbd4fd933f7820c8ed7b39efe8f58c1063e9a31d326e',
            '1.7.0':  '9642c62bba6d47a6103729d5617f031ce61b68d34735a9873fa99f7d8769cce4',
            '1.6.0':  '8c6897ed37ef6fd2890b176afa65306cc8943e3c770c9530a701f1aefd3942b1',
            '1.5.0':  'bad9d1a96bd423662f247ae9dd5f61846aae668ad2b8c332e72a8cf407f473e4',
            '1.4.0':  '7256617aec7c106be2aa3c5df0a2e613b13ec55e6237ab612bb4164719e09e21',
            '1.3.0':  'bfeac876e22cc5fe63a250644ce1a6f3892c13a5461131a881419bd06fcb2011',
            '1.2.0':  '0d471e672fac5a450ae5507b335fda2efc0b22ea9fb7f215c6a9c466dafa2661',
            '1.1.0':  'ac802916da3f9c431377c00b864a517bc356859495b7a8a123ce2c532ee8fa83',
            '1.0.0':  '4b18ea61f2fda53d0f2e59ddf651e96a08ed31205db15e82fa514d434c5594d8'
        }
    }

    rust_archs = {
        'x86_64-unknown-linux-gnu': [
            { 'platform': 'linux', 'target': 'x86_64:' },
            { 'platform': 'cray', 'target': 'x86_64:' }
        ],
        'powerpc64le-unknown-linux-gnu': [
            { 'platform': 'linux', 'target': 'ppc64le:' },
            { 'platform': 'cray', 'target': 'ppc64le:' }
        ],
        'x86_64-apple-darwin': [
            { 'platform': 'darwin', 'target': 'x86_64:' }
        ]
    }

    for rust_target, rust_versions in iteritems(rust_releases):
        for rust_arch in rust_archs[rust_target]:
            for rust_version, rust_sha256 in iteritems(rust_versions):
                resource(
                    name='rust-{version}-{target}'.format(
                        version=rust_version,
                        target=rust_target
                    ),
                    url='https://static.rust-lang.org/dist/rust-{version}-{target}.tar.gz'.format(
                        version=rust_version,
                        target=rust_target
                    ),
                    sha256=rust_sha256,
                    destination='spack_bootstrap_stage',
                    when='@{version} platform={platform} target={target}'.format(
                        version=rust_version,
                        platform=rust_arch['platform'],
                        target=rust_arch['target']
                    )
                )

    def configure(self, spec, prefix):
        bootstrapping_install = Executable('./spack_bootstrap_stage/install.sh')
        # install into the staging area
        bootstrapping_install('--prefix=spack_bootstrap')
