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

    # The `x.py` bootstrapping script did not exist prior to Rust 1.17. It
    # would be possible to support both, but for simplicitly, we only support
    # Rust 1.17 and newer
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

    # The Rust bootstrapping process requires a bootstrapping compiler. The
    # easiest way to do this is to download the binary distribution of the
    # same version of the compiler and build with that.
    #
    # This dictionary contains a version: hash dictionary for each supported
    # Rust target.
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
            '1.17.0': 'bbb0e249a7a3e8143b569706c7d2e7e5f51932c753b7fd26c58ccd2015b02c6b'
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
            '1.17.0': '2dda1fff20aecd7b208babfd45f70c608978fe2594916d1448e42757bb7e759f'
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
            '1.17.0': '1689060c07ec727e9756f19c9373045668471ab56fd8f53e92701150bbe2032b'
        }
    }

    # This dictionary maps Rust target architectures to Spack constraints that
    # match that target.
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

    # This loop generates resources for each binary distribution, and maps
    # them to the version of the compiler they bootstrap. This is in place
    # of listing each resource explicitly, which would be potentially even
    # more verbose.
    #
    # NOTE: This loop should technically specify the architecture to be the
    # _host_ architecture, not the target architecture, in order to support
    # cross compiling. I'm not sure Spack provides a way to specify a
    # distinction in the when clause, though.
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

    # This routine returns the target architecture we intend to build for.
    def get_rust_target(self):
        if self.spec.satisfies('platform=linux target=x86_64:') or \
           self.spec.satisfies('platform=cray target=x86_64:'):
            return 'x86_64-unknown-linux-gnu'
        elif self.spec.satisfies('platform=linux target=ppc64le:'):
            return 'powerpc64le-unknown-linux-gnu'
        elif self.spec.satisfies('platform=darwin target=x86_64:'):
            return 'x86_64-apple-darwin'
        else:
            raise InstallError(
                "rust-binary is not supported for '{0}'".format(
                    self.spec.architecture
                ))

    def configure(self, spec, prefix):
        target = self.get_rust_target()
        # See the NOTE above the resource loop - should be host architecture,
        # not target aarchitecture if we're to support cross-compiling.
        bootstrapping_install = Executable(
            './spack_bootstrap_stage/rust-{version}-{target}/install.sh'.format(
                version=spec.version,
                target=target
            )
        )
        # install into the staging area
        bootstrapping_install('--prefix={}'.format(
            join_path(self.stage.source_path, 'spack_bootstrap')
        ))

        boot_bin = join_path(self.stage.source_path, 'spack_bootstrap/bin')

        # Always build rustc and cargo
        tools = ['rustc', 'cargo']
        # Only make additional components available in 'rust-bootstrap'
        if '+rustfmt' in self.spec:
            tools.append('rustfmt')
        if '+analysis' in self.spec:
            tools.append('analysis')
        if '@1.33: +clippy' in self.spec:
            tools.append('clippy')
        if '+rls' in self.spec:
            tools.append('rls')
        if '+src' in self.spec:
            tools.append('src')

        ar = which('ar', required=True)

        with open('config.toml', 'w') as out_file:
            out_file.write("""\
[build]
cargo = "{cargo}"
rustc = "{rustc}"
docs = false
vendor = true
extended = true
verbose = 2
tools = {tools}

[rust]
channel = "stable"
rpath = true
# This is a temporary fix due to rust 1.42 breaking self bootstrapping
# See: https://github.com/rust-lang/rust/issues/69953
#
# In general, this should be safe because bootstrapping typically ensures
# everything but the bootstrapping script is warning free for the latest set
# of warning.
deny-warnings = false

[target.{target}]
ar = "{ar}"

[install]
prefix = "{prefix}"
sysconfdir = "etc"
""".format(
                cargo=join_path(boot_bin, 'cargo'),
                rustc=join_path(boot_bin, 'rustc'),
                prefix=prefix,
                target=target,
                ar=ar.path,
                tools=tools
            )
            )

    def build(self, spec, prefix):
        x_py = Executable('./x.py')
        x_py(
            'build',
            extra_env={
                # vendored libgit2 wasn't correctly building (couldn't find the
                # vendored libssh2), so let's just have spack build it
                'LIBSSH2_SYS_USE_PKG_CONFIG': '1',
                'LIBGIT2_SYS_USE_PKG_CONFIG': '1'
            })

    def install(self, spec, prefix):
        x_py = Executable('./x.py')
        x_py('install')
