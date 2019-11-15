# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Llvm(CMakePackage):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do
       with traditional virtual machines, though it does provide helpful
       libraries that can be used to build them. The name "LLVM" itself
       is not an acronym; it is the full name of the project.
    """

    homepage = 'http://llvm.org/'
    url = 'http://llvm.org/releases/3.7.1/llvm-3.7.1.src.tar.xz'
    list_url = 'http://releases.llvm.org/download.html'

    family = 'compiler'  # Used by lmod

    # currently required by mesa package
    version('3.0', sha256='519eb11d3499ce99c6ffdb8718651fc91425ed7690eac91c8d6853474f7c0477',
            url='http://llvm.org/releases/3.0/llvm-3.0.tar.gz')

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    variant('clang', default=True,
            description="Build the LLVM C/C++/Objective-C compiler frontend")

    # TODO: The current version of this package unconditionally disables CUDA.
    #       Better would be to add a "cuda" variant that:
    #        - Adds dependency on the "cuda" package when enabled
    #        - Sets the necessary CMake flags when enabled
    #        - Disables CUDA (as this current version does) only when the
    #          variant is also disabled.

    # variant('cuda', default=False,
    #         description="Build the LLVM with CUDA features enabled")

    variant('lldb', default=True, description="Build the LLVM debugger")
    variant('lld', default=True, description="Build the LLVM linker")
    variant('internal_unwind', default=True,
            description="Build the libcxxabi libunwind")
    variant('polly', default=True,
            description="Build the LLVM polyhedral optimization plugin, "
            "only builds for 3.7.0+")
    variant('libcxx', default=True,
            description="Build the LLVM C++ standard library")
    variant('compiler-rt', default=True,
            description="Build LLVM compiler runtime, including sanitizers")
    variant('gold', default=True,
            description="Add support for LTO with the gold linker plugin")
    variant('shared_libs', default=False,
            description="Build all components as shared libraries, faster, "
            "less memory to build, less stable")
    variant('link_dylib', default=False,
            description="Build and link the libLLVM shared library rather "
            "than static")
    variant('all_targets', default=False,
            description="Build all supported targets, default targets "
            "<current arch>,NVPTX,AMDGPU,CppBackend")
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('omp_tsan', default=False,
            description="Build with OpenMP capable thread sanitizer")
    variant('python', default=False, description="Install python bindings")
    extends('python', when='+python')

    # Build dependency
    depends_on('cmake@3.4.3:', type='build')
    depends_on('python@2.7:2.8', when='@:4.999 ~python', type='build')
    depends_on('python', when='@5: ~python', type='build')

    # Universal dependency
    depends_on('python@2.7:2.8', when='@:4.999+python')
    depends_on('python', when='@5:+python')

    # openmp dependencies
    depends_on('perl-data-dumper', type=('build'))

    # lldb dependencies
    depends_on('ncurses', when='+lldb')
    depends_on('swig', when='+lldb')
    depends_on('libedit', when='+lldb')
    depends_on('py-six', when='@5.0.0: +lldb +python')

    # gold support
    depends_on('binutils+gold', when='+gold')

    # polly plugin
    depends_on('gmp', when='@:3.6.999 +polly')
    depends_on('isl', when='@:3.6.999 +polly')

    base_url = 'http://llvm.org/releases/%%(version)s/%(pkg)s-%%(version)s.src.tar.xz'
    llvm_url = base_url % {'pkg': 'llvm'}
    # Flang uses its own fork of llvm.
    flang_llvm_url = 'https://github.com/flang-compiler/llvm.git'

    resources = {
        'compiler-rt': {
            'url': base_url % {'pkg': 'compiler-rt'},
            'destination': 'projects',
            'placement': 'compiler-rt',
            'variant': '+compiler-rt',
        },
        'openmp': {
            'url': base_url % {'pkg': 'openmp'},
            'destination': 'projects',
            'placement': 'openmp',
            'variant': '+clang',
        },
        'libcxx': {
            'url': base_url % {'pkg': 'libcxx'},
            'destination': 'projects',
            'placement': 'libcxx',
            'variant': '+libcxx',
        },
        'libcxxabi': {
            'url':  base_url % {'pkg': 'libcxxabi'},
            'destination': 'projects',
            'placement': 'libcxxabi',
            'variant': '+libcxx',
        },
        'cfe': {
            'url':  base_url % {'pkg': 'cfe'},
            'destination': 'tools',
            'placement': 'clang',
            'variant': '+clang',
        },
        'clang-tools-extra': {
            'url':  base_url % {'pkg': 'clang-tools-extra'},
            'destination': 'tools/clang/tools',
            'placement': 'extra',
            'variant': '+clang',
        },
        'lldb': {
            'url':  base_url % {'pkg': 'lldb'},
            'destination': 'tools',
            'placement': 'lldb',
            'variant': '+lldb',
        },
        'lld': {
            'url':  base_url % {'pkg': 'lld'},
            'destination': 'tools',
            'placement': 'lld',
            'variant': '+lld',
        },
        'polly': {
            'url':  base_url % {'pkg': 'polly'},
            'destination': 'tools',
            'placement': 'polly',
            'variant': '+polly',
        },
        'libunwind': {
            'url':  base_url % {'pkg': 'libunwind'},
            'destination': 'projects',
            'placement': 'libunwind',
            'variant': '+internal_unwind',
        },
    }
    releases = [
        {
            'version': 'develop',
            'repo': 'http://llvm.org/svn/llvm-project/llvm/trunk',
            'resources': {
                'compiler-rt': 'http://llvm.org/svn/llvm-project/compiler-rt/trunk',
                'openmp': 'http://llvm.org/svn/llvm-project/openmp/trunk',
                'polly': 'http://llvm.org/svn/llvm-project/polly/trunk',
                'libcxx': 'http://llvm.org/svn/llvm-project/libcxx/trunk',
                'libcxxabi': 'http://llvm.org/svn/llvm-project/libcxxabi/trunk',
                'cfe': 'http://llvm.org/svn/llvm-project/cfe/trunk',
                'clang-tools-extra': 'http://llvm.org/svn/llvm-project/clang-tools-extra/trunk',
                'lldb': 'http://llvm.org/svn/llvm-project/lldb/trunk',
                'lld': 'http://llvm.org/svn/llvm-project/lld/trunk',
                'libunwind': 'http://llvm.org/svn/llvm-project/libunwind/trunk',
            }
        },
        {
            'version': '9.0.0',
            'sha256': 'd6a0565cf21f22e9b4353b2eb92622e8365000a9e90a16b09b56f8157eabfe84',
            'resources': {
                'compiler-rt': '56e4cd96dd1d8c346b07b4d6b255f976570c6f2389697347a6c3dcb9e820d10e',
                'openmp': '9979eb1133066376cc0be29d1682bc0b0e7fb541075b391061679111ae4d3b5b',
                'polly': 'a4fa92283de725399323d07f18995911158c1c5838703f37862db815f513d433',
                'libcxx': '3c4162972b5d3204ba47ac384aa456855a17b5e97422723d4758251acf1ed28c',
                'libcxxabi': '675041783565c906ac2f7f8b2bc5c40f14d871ecfa8ade34855aa18de95530e9',
                'cfe': '7ba81eef7c22ca5da688fdf9d88c20934d2d6b40bfe150ffd338900890aa4610',
                'clang-tools-extra': 'ea1c86ce352992d7b6f6649bc622f6a2707b9f8b7153e9f9181a35c76aa3ac10',
                'lldb': '1e4c2f6a1f153f4b8afa2470d2e99dab493034c1ba8b7ffbbd7600de016d0794',
                'lld': '31c6748b235d09723fb73fea0c816ed5a3fab0f96b66f8fbc546a0fcc8688f91',
                'libunwind': '976a8d09e1424fb843210eecec00a506b956e6c31adda3b0d199e945be0d0db2'
            }
        },
        {
            'version': '8.0.0',
            'sha256': '8872be1b12c61450cacc82b3d153eab02be2546ef34fa3580ed14137bb26224c',
            'resources': {
                'compiler-rt': 'b435c7474f459e71b2831f1a4e3f1d21203cb9c0172e94e9d9b69f50354f21b1',
                'openmp': 'f7b1705d2f16c4fc23d6531f67d2dd6fb78a077dd346b02fed64f4b8df65c9d5',
                'polly': 'e3f5a3d6794ef8233af302c45ceb464b74cdc369c1ac735b6b381b21e4d89df4',
                'libcxx': 'c2902675e7c84324fb2c1e45489220f250ede016cc3117186785d9dc291f9de2',
                'libcxxabi': 'c2d6de9629f7c072ac20ada776374e9e3168142f20a46cdb9d6df973922b07cd',
                'cfe': '084c115aab0084e63b23eee8c233abb6739c399e29966eaeccfc6e088e0b736b',
                'clang-tools-extra': '4f00122be408a7482f2004bcf215720d2b88cf8dc78b824abb225da8ad359d4b',
                'lldb': '49918b9f09816554a20ac44c5f85a32dc0a7a00759b3259e78064d674eac0373',
                'lld': '9caec8ec922e32ffa130f0fb08e4c5a242d7e68ce757631e425e9eba2e1a6e37',
                'libunwind': 'ff243a669c9cef2e2537e4f697d6fb47764ea91949016f2d643cb5d8286df660'
            }
        },
        {
            'version': '7.0.1',
            'sha256': 'a38dfc4db47102ec79dcc2aa61e93722c5f6f06f0a961073bd84b78fb949419b',
            'resources': {
                'compiler-rt': '782edfc119ee172f169c91dd79f2c964fb6b248bd9b73523149030ed505bbe18',
                'openmp': 'bf16b78a678da67d68405214ec7ee59d86a15f599855806192a75dcfca9b0d0c',
                'polly': '1bf146842a09336b9c88d2d76c2d117484e5fad78786821718653d1a9d57fb71',
                'libcxx': '020002618b319dc2a8ba1f2cba88b8cc6a209005ed8ad29f9de0c562c6ebb9f1',
                'libcxxabi': '8168903a157ca7ab8423d3b974eaa497230b1564ceb57260be2bd14412e8ded8',
                'cfe': 'a45b62dde5d7d5fdcdfa876b0af92f164d434b06e9e89b5d0b1cbc65dfe3f418',
                'clang-tools-extra': '4c93c7d2bb07923a8b272da3ef7914438080aeb693725f4fc5c19cd0e2613bed',
                'lldb': '76b46be75b412a3d22f0d26279306ae7e274fe4d7988a2184c529c38a6a76982',
                'lld': '8869aab2dd2d8e00d69943352d3166d159d7eae2615f66a684f4a0999fc74031',
                'libunwind': '89c852991dfd9279dbca9d5ac10b53c67ad7d0f54bbab7156e9f057a978b5912'
            }
        },
        {
            'version': '7.0.0',
            'sha256': '8bc1f844e6cbde1b652c19c1edebc1864456fd9c78b8c1bea038e51b363fe222',
            'resources': {
                'compiler-rt': 'bdec7fe3cf2c85f55656c07dfb0bd93ae46f2b3dd8f33ff3ad6e7586f4c670d6',
                'openmp': '30662b632f5556c59ee9215c1309f61de50b3ea8e89dcc28ba9a9494bba238ff',
                'polly': '919810d3249f4ae79d084746b9527367df18412f30fe039addbf941861c8534b',
                'libcxx': '9b342625ba2f4e65b52764ab2061e116c0337db2179c6bce7f9a0d70c52134f0',
                'libcxxabi': '9b45c759ff397512eae4d938ff82827b1bd7ccba49920777e5b5e460baeb245f',
                'cfe': '550212711c752697d2f82c648714a7221b1207fd9441543ff4aa9e3be45bba55',
                'clang-tools-extra': '937c5a8c8c43bc185e4805144744799e524059cac877a44d9063926cd7a19dbe',
                'lldb': '7ff6d8fee49977d25b3b69be7d22937b92592c7609cf283ed0dcf9e5cd80aa32',
                'lld': 'fbcf47c5e543f4cdac6bb9bbbc6327ff24217cd7eafc5571549ad6d237287f9c',
                'libunwind': '50aee87717421e70450f1e093c6cd9a27f2b111025e1e08d64d5ace36e338a9c'
            }
        },
        {
            'version': '6.0.1',
            'sha256': 'b6d6c324f9c71494c0ccaf3dac1f16236d970002b42bb24a6c9e1634f7d0f4e2',
            'resources': {
                'compiler-rt': 'f4cd1e15e7d5cb708f9931d4844524e4904867240c306b06a4287b22ac1c99b9',
                'openmp': '66afca2b308351b180136cf899a3b22865af1a775efaf74dc8a10c96d4721c5a',
                'polly': 'e7765fdf6c8c102b9996dbb46e8b3abc41396032ae2315550610cf5a1ecf4ecc',
                'libcxx': '7654fbc810a03860e6f01a54c2297a0b9efb04c0b9aa0409251d9bdb3726fc67',
                'libcxxabi': '209f2ec244a8945c891f722e9eda7c54a5a7048401abd62c62199f3064db385f',
                'cfe': '7c243f1485bddfdfedada3cd402ff4792ea82362ff91fbdac2dae67c6026b667',
                'clang-tools-extra': '0d2e3727786437574835b75135f9e36f861932a958d8547ced7e13ebdda115f1',
                'lldb': '6b8573841f2f7b60ffab9715c55dceff4f2a44e5a6d590ac189d20e8e7472714',
                'lld': 'e706745806921cea5c45700e13ebe16d834b5e3c0b7ad83bf6da1f28b0634e11',
                'libunwind': 'a8186c76a16298a0b7b051004d0162032b9b111b857fbd939d71b0930fd91b96'
            }
        },
        {
            'version': '6.0.0',
            'sha256': '1ff53c915b4e761ef400b803f07261ade637b0c269d99569f18040f3dcee4408',
            'resources': {
                'compiler-rt': 'd0cc1342cf57e9a8d52f5498da47a3b28d24ac0d39cbc92308781b3ee0cea79a',
                'openmp': '7c0e050d5f7da3b057579fb3ea79ed7dc657c765011b402eb5bbe5663a7c38fc',
                'polly': '47e493a799dca35bc68ca2ceaeed27c5ca09b12241f87f7220b5f5882194f59c',
                'libcxx': '70931a87bde9d358af6cb7869e7535ec6b015f7e6df64def6d2ecdd954040dd9',
                'libcxxabi': '91c6d9c5426306ce28d0627d6a4448e7d164d6a3f64b01cb1d196003b16d641b',
                'cfe': 'e07d6dd8d9ef196cfc8e8bb131cbd6a2ed0b1caf1715f9d05b0f0eeaddb6df32',
                'clang-tools-extra': '053b424a4cd34c9335d8918734dd802a8da612d13a26bbb88fcdf524b2d989d2',
                'lldb': '46f54c1d7adcd047d87c0179f7b6fa751614f339f4f87e60abceaa45f414d454',
                'lld': '6b8c4a833cf30230c0213d78dbac01af21387b298225de90ab56032ca79c0e0b',
                'libunwind': '256c4ed971191bde42208386c8d39e5143fa4afd098e03bd2c140c878c63f1d6'
            }
        },
        {
            'version': '5.0.2',
            'sha256': 'd522eda97835a9c75f0b88ddc81437e5edbb87dc2740686cb8647763855c2b3c',
            'resources': {
                'compiler-rt': '3efe9ddf3f69e0c0a45cde57ee93911f36f3ab5f2a7f6ab8c8efb3db9b24ed46',
                'openmp': '39ca542c540608d95d3299a474836a7b5f8377bcc5a68493379872738c28565c',
                'polly': 'dda84e48b2195768c4ef25893edd5eeca731bed7e80a2376119dfbc3350e91b8',
                'libcxx': '6edf88e913175536e1182058753fff2365e388e017a9ec7427feb9929c52e298',
                'libcxxabi': '1bbf9bf2c92a4d627dd7bb7a15166acecae924b19898dc0573244f9d533a978a',
                'cfe': 'fa9ce9724abdb68f166deea0af1f71ca0dfa9af8f7e1261f2cae63c280282800',
                'clang-tools-extra': 'a3362a854ba4a60336b21a95612f647f4b6de0afd88858f2420e41c5a31b0b05',
                'lldb': '78ba05326249b4d7577db56d16b2a7ffea43fc51e8592b0a1ac4d2ef87514216',
                'lld': '46456d72ec411c6d5327ad3fea1358296f0dfe508caf1fa63ce4184f652e07aa',
                'libunwind': '706e43c69c7be0fdeb55ebdf653cf47ca77e471d1584f1dbf12a568a93df9928',
            }
        },
        {
            'version': '5.0.1',
            'sha256': '5fa7489fc0225b11821cab0362f5813a05f2bcf2533e8a4ea9c9c860168807b0',
            'resources': {
                'compiler-rt': '4edd1417f457a9b3f0eb88082530490edf3cf6a7335cdce8ecbc5d3e16a895da',
                'openmp': 'adb635cdd2f9f828351b1e13d892480c657fb12500e69c70e007bddf0fca2653',
                'polly': '9dd52b17c07054aa8998fc6667d41ae921430ef63fa20ae130037136fdacf36e',
                'libcxx': 'fa8f99dd2bde109daa3276d529851a3bce5718d46ce1c5d0806f46caa3e57c00',
                'libcxxabi': '5a25152cb7f21e3c223ad36a1022faeb8a5ac27c9e75936a5ae2d3ac48f6e854',
                'cfe': '135f6c9b0cd2da1aff2250e065946258eb699777888df39ca5a5b4fe5e23d0ff',
                'clang-tools-extra': '9aada1f9d673226846c3399d13fab6bba4bfd38bcfe8def5ee7b0ec24f8cd225',
                'lldb': 'b7c1c9e67975ca219089a3a6a9c77c2d102cead2dc38264f2524aa3326da376a',
                'lld': 'd5b36c0005824f07ab093616bdff247f3da817cae2c51371e1d1473af717d895',
                'libunwind': '6bbfbf6679435b858bd74bdf080386d084a76dfbf233fb6e47b2c28e0872d0fe',
            }
        },
        {
            'version': '5.0.0',
            'sha256': 'e35dcbae6084adcf4abb32514127c5eabd7d63b733852ccdb31e06f1373136da',
            'resources': {
                'compiler-rt': 'd5ad5266462134a482b381f1f8115b6cad3473741b3bb7d1acc7f69fd0f0c0b3',
                'openmp': 'c0ef081b05e0725a04e8711d9ecea2e90d6c3fbb1622845336d3d095d0a3f7c5',
                'polly': '44694254a2b105cec13ce0560f207e8552e6116c181b8d21bda728559cf67042',
                'libcxx': 'eae5981e9a21ef0decfcac80a1af584ddb064a32805f95a57c7c83a5eb28c9b1',
                'libcxxabi': '176918c7eb22245c3a5c56ef055e4d69f5345b4a98833e0e8cb1a19cab6b8911',
                'cfe': '019f23c2192df793ac746595e94a403908749f8e0c484b403476d2611dd20970',
                'clang-tools-extra': '87d078b959c4a6e5ff9fd137c2f477cadb1245f93812512996f73986a6d973c6',
                'lldb': 'c0a0ca32105e9881d86b7ca886220147e686edc97fdb9f3657c6659dc6568b7d',
                'lld': '399a7920a5278d42c46a7bf7e4191820ec2301457a7d0d4fcc9a4ac05dd53897',
                'libunwind': '9a70e2333d54f97760623d89512c4831d6af29e78b77a33d824413ce98587f6f',
            }
        },
        {
            'version': '4.0.1',
            'sha256': 'da783db1f82d516791179fe103c71706046561f7972b18f0049242dee6712b51',
            'resources': {
                'compiler-rt': 'a3c87794334887b93b7a766c507244a7cdcce1d48b2e9249fc9a94f2c3beb440',
                'openmp': 'ec693b170e0600daa7b372240a06e66341ace790d89eaf4a843e8d56d5f4ada4',
                'polly': 'b443bb9617d776a7d05970e5818aa49aa2adfb2670047be8e9f242f58e84f01a',
                'libcxx': '520a1171f272c9ff82f324d5d89accadcec9bc9f3c78de11f5575cdb99accc4c',
                'libcxxabi': '8f08178989a06c66cd19e771ff9d8ca526dd4a23d1382d63e416c04ea9fa1b33',
                'cfe': '61738a735852c23c3bdbe52d035488cdb2083013f384d67c1ba36fabebd8769b',
                'clang-tools-extra': '35d1e64efc108076acbe7392566a52c35df9ec19778eb9eb12245fc7d8b915b6',
                'lldb': '8432d2dfd86044a0fc21713e0b5c1d98e1d8aad863cf67562879f47f841ac47b',
                'lld': '63ce10e533276ca353941ce5ab5cc8e8dcd99dbdd9c4fa49f344a212f29d36ed',
                'libunwind': '3b072e33b764b4f9b5172698e080886d1f4d606531ab227772a7fc08d6a92555',
            }
        },
        {
            'version': '4.0.0',
            'sha256': '8d10511df96e73b8ff9e7abbfb4d4d432edbdbe965f1f4f07afaf370b8a533be',
            'resources': {
                'compiler-rt': 'd3f25b23bef24c305137e6b44f7e81c51bbec764c119e01512a9bd2330be3115',
                'openmp': 'db55d85a7bb289804dc42fc5c8e35ca24dfc3885782261b675a194fd7e206e26',
                'polly': '27a5dbf95e8aa9e0bbe3d6c5d1e83c92414d734357aa0d6c16020a65dc4dcd97',
                'libcxx': '4f4d33c4ad69bf9e360eebe6b29b7b19486948b1a41decf89d4adec12473cf96',
                'libcxxabi': 'dca9cb619662ad2d3a0d685c4366078345247218c3702dd35bcaaa23f63481d8',
                'cfe': 'cea5f88ebddb30e296ca89130c83b9d46c2d833685e2912303c828054c4dc98a',
                'clang-tools-extra': '41b7d37eb128fd362ab3431be5244cf50325bb3bb153895735c5bacede647c99',
                'lldb': '2dbd8f05c662c1c9f11270fc9d0c63b419ddc988095e0ad107ed911cf882033d',
                'lld': '33e06457b9ce0563c89b11ccc7ccabf9cff71b83571985a5bf8684c9150e7502',
                'libunwind': '0755efa9f969373d4d543123bbed4b3f9a835f6302875c1379c5745857725973',
            }
        },
        {
            'version': '3.9.1',
            'sha256': '1fd90354b9cf19232e8f168faf2220e79be555df3aa743242700879e8fd329ee',
            'resources': {
                'compiler-rt': 'd30967b1a5fa51a2503474aacc913e69fd05ae862d37bf310088955bdb13ec99',
                'openmp': 'd23b324e422c0d5f3d64bae5f550ff1132c37a070e43c7ca93991676c86c7766',
                'polly': '9ba5e61fc7bf8c7435f64e2629e0810c9b1d1b03aa5b5605b780d0e177b4cb46',
                'libcxx': '25e615e428f60e651ed09ffd79e563864e3f4bc69a9e93ee41505c419d1a7461',
                'libcxxabi': '920d8be32e6f5574a3fb293f93a31225eeba15086820fcb942155bf50dc029e2',
                'cfe': 'e6c4cebb96dee827fa0470af313dff265af391cb6da8d429842ef208c8f25e63',
                'clang-tools-extra': '29a5b65bdeff7767782d4427c7c64d54c3a8684bc6b217b74a70e575e4813635',
                'lldb': '7e3311b2a1f80f4d3426e09f9459d079cab4d698258667e50a46dccbaaa460fc',
                'lld': '48e128fabb2ddaee64ecb8935f7ac315b6e68106bc48aeaf655d179c65d87f34',
                'libunwind': '0b0bc73264d7ab77d384f8a7498729e3c4da8ffee00e1c85ad02a2f85e91f0e6',
            }
        },
        {
            'version': '3.9.0',
            'sha256': '66c73179da42cee1386371641241f79ded250e117a79f571bbd69e56daa48948',
            'resources': {
                'compiler-rt': 'e0e5224fcd5740b61e416c549dd3dcda92f10c524216c1edb5e979e42078a59a',
                'openmp': 'df88f90d7e5b5e9525a35fa2e2b93cbbb83c4882f91df494e87ee3ceddacac91',
                'polly': 'ef0dd25010099baad84597cf150b543c84feac2574d055d6780463d5de8cd97e',
                'libcxx': 'd0b38d51365c6322f5666a2a8105785f2e114430858de4c25a86b49f227f5b06',
                'libcxxabi': 'b037a92717856882e05df57221e087d7d595a2ae9f170f7bc1a23ec7a92c8019',
                'cfe': '7596a7c7d9376d0c89e60028fe1ceb4d3e535e8ea8b89e0eb094e0dcb3183d28',
                'clang-tools-extra': '5b7aec46ec8e999ec683c87ad744082e1133781ee4b01905b4bdae5d20785f14',
                'lldb': '61280e07411e3f2b4cca0067412b39c16b0a9edd19d304d3fc90249899d12384',
                'lld': '986e8150ec5f457469a20666628bf634a5ca992a53e157f3b69dbc35056b32d9',
                'libunwind': '66675ddec5ba0d36689757da6008cb2596ee1a9067f4f598d89ce5a3b43f4c2b',
            }
        },
        {
            'version': '3.8.1',
            'sha256': '6e82ce4adb54ff3afc18053d6981b6aed1406751b8742582ed50f04b5ab475f9',
            'resources': {
                'compiler-rt': '0df011dae14d8700499dfc961602ee0a9572fef926202ade5dcdfe7858411e5c',
                'openmp': '68fcde6ef34e0275884a2de3450a31e931caf1d6fda8606ef14f89c4123617dc',
                'polly': '453c27e1581614bb3b6351bf5a2da2939563ea9d1de99c420f85ca8d87b928a2',
                'libcxx': '77d7f3784c88096d785bd705fa1bab7031ce184cd91ba8a7008abf55264eeecc',
                'libcxxabi': 'e1b55f7be3fad746bdd3025f43e42d429fb6194aac5919c2be17c4a06314dae1',
                'cfe': '4cd3836dfb4b88b597e075341cae86d61c63ce3963e45c7fe6a8bf59bb382cdf',
                'clang-tools-extra': '664a5c60220de9c290bf2a5b03d902ab731a4f95fe73a00856175ead494ec396',
                'lldb': '349148116a47e39dcb5d5042f10d8a6357d2c865034563283ca512f81cdce8a3',
                'lld': '2bd9be8bb18d82f7f59e31ea33b4e58387dbdef0bc11d5c9fcd5ce9a4b16dc00',
                'libunwind': '21e58ce09a5982255ecf86b86359179ddb0be4f8f284a95be14201df90e48453',
            }
        },
        {
            'version': '3.8.0',
            'sha256': '555b028e9ee0f6445ff8f949ea10e9cd8be0d084840e21fbbe1d31d51fc06e46',
            'resources': {
                'compiler-rt': 'c8d3387e55f229543dac1941769120f24dc50183150bf19d1b070d53d29d56b0',
                'openmp': '92510e3f62e3de955e3a0b6708cebee1ca344d92fb02369cba5fdd5c68f773a0',
                'polly': '84cbabc0b6a10a664797907d291b6955d5ea61aef04e3f3bb464e42374d1d1f2',
                'libcxx': '36804511b940bc8a7cefc7cb391a6b28f5e3f53f6372965642020db91174237b',
                'libcxxabi': 'c5ee0871aff6ec741380c4899007a7d97f0b791c81df69d25b744eebc5cee504',
                'cfe': '04149236de03cf05232d68eb7cb9c50f03062e339b68f4f8a03b650a11536cf9',
                'clang-tools-extra': 'afbda810106a6e64444bc164b921be928af46829117c95b996f2678ce4cb1ec4',
                'lldb': 'e3f68f44147df0433e7989bf6ed1c58ff28d7c68b9c47553cb9915f744785a35',
                'lld': '94704dda228c9f75f4403051085001440b458501ec97192eee06e8e67f7f9f0c',
                'libunwind': 'af3eaf39ecdc3b9e89863fb62e1aa3c135cfde7e9415424e4e396d7486a9422b',
            }
        },
        {
            'version': '3.7.1',
            'sha256': 'be7794ed0cec42d6c682ca8e3517535b54555a3defabec83554dbc74db545ad5',
            'resources': {
                'compiler-rt': '9d4769e4a927d3824bcb7a9c82b01e307c68588e6de4e7f04ab82d82c5af8181',
                'openmp': '9a702e20c247014f6de8c45b738c6ea586eca0559304520f565ac9a7cba4bf9a',
                'polly': 'ce9273ad315e1904fd35dc64ac4375fd592f3c296252ab1d163b9ff593ec3542',
                'libcxx': '357fbd4288ce99733ba06ae2bec6f503413d258aeebaab8b6a791201e6f7f144',
                'libcxxabi': 'a47faaed90f577da8ca3b5f044be9458d354a53fab03003a44085a912b73ab2a',
                'cfe': '56e2164c7c2a1772d5ed2a3e57485ff73ff06c97dff12edbeea1acc4412b0674',
                'clang-tools-extra': '4a91edaccad1ce984c7c49a4a87db186b7f7b21267b2b03bcf4bd7820715bc6b',
                'lldb': '9a0bc315ef55f44c98cdf92d064df0847f453ed156dd0ef6a87e04f5fd6a0e01',
                'lld': 'a929cb44b45e3181a0ad02d8c9df1d3fc71e001139455c6805f3abf2835ef3ac',
                'libunwind': 'b69f445253c2e5d3c8be6abe379372a52d223e0e5a5520b79983866c03f949fb',
            }
        },
        {
            'version': '3.7.0',
            'sha256': 'ab45895f9dcdad1e140a3a79fd709f64b05ad7364e308c0e582c5b02e9cc3153',
            'resources': {
                'compiler-rt': '227fa998520bc94974a428dc8e7654d9bdf277e5bc70d4064ebc05691bd62b0b',
                'openmp': '8d8a224e5689596a35652fda87e4be29853c4b85fbc7a6562019badfad779f2a',
                'polly': '3e5f3f4dc141c7d25b36b910d48c7da74ecc92f10cea5b568c909623d6067edf',
                'libcxx': 'c18f3c8333cd7e678c1424a57fe5e25efe740ca7caf62ac67152b4723f3ad08e',
                'libcxxabi': '48b074fd334958b2d8bab893c897a0c8258328782cdec2d229c7bce432b49beb',
                'cfe': '4ed740c5a91df1c90a4118c5154851d6a475f39a91346bdf268c1c29c13aa1cc',
                'clang-tools-extra': '8ae8a0a3a96b7a700412d67df0af172cb2fc1326beec575fcc0f71d2e72709cd',
                'lldb': 'f4d7505bc111044eaa4033af012221e492938405b62522b8e3e354c20c4b71e9',
                'lld': 'ddb658b789c501efbe4f54ff8ced2c07cd9ff686c92445d8a1ab2cd5dbd837ed',
                'libunwind': '6a600f30b9f3a54a1faf8c2dfd12522a0c90eb65f1aad63fec540aa27bcaca5b',
            }
        },
        {
            'version': '3.6.2',
            'sha256': 'f60dc158bfda6822de167e87275848969f0558b3134892ff54fced87e4667b94',
            'resources': {
                'compiler-rt': '0f2ff37d80a64575fecd8cf0d5c50f7ac1f837ddf700d1855412bb7547431d87',
                'openmp': '9d9640e7fc76ef531b5e919d79ee241cb35aa599fd1cac97c52ca49c97778f8e',
                'libcxx': '52f3d452f48209c9df1792158fdbd7f3e98ed9bca8ebb51fcd524f67437c8b81',
                'libcxxabi': '6fb48ce5a514686b9b75e73e59869f782ed374a86d71be8423372e4b3329b09b',
                'cfe': 'ae9180466a23acb426d12444d866b266ff2289b266064d362462e44f8d4699f3',
                'clang-tools-extra': '6a0ec627d398f501ddf347060f7a2ccea4802b2494f1d4fd7bda3e0442d04feb',
                'lldb': '940dc96b64919b7dbf32c37e0e1d1fc88cc18e1d4b3acf1e7dfe5a46eb6523a9',
                'lld': '43f553c115563600577764262f1f2fac3740f0c639750f81e125963c90030b33',
            }
        },
        {
            'version': '3.5.1',
            'sha256': 'bf3275d2d7890015c8d8f5e6f4f882f8cf3bf51967297ebe74111d6d8b53be15',
            'resources': {
                'compiler-rt': 'adf4b526f33e681aff5961f0821f5b514d3fc375410008842640b56a2e6a837a',
                'openmp': '43ea73eeac3045127cf01b496d714b559e42311043480682049e8fea243eac55',
                'libcxx': 'a16d0ae0c0cf2c8cebb94fafcb907022cd4f8579ebac99a4c9919990a37ad475',
                'libcxxabi': '7ff14fdce0ed7bfcc532c627c7a2dc7876dd8a3d788b2aa201d3bbdc443d06a3',
                'cfe': '6773f3f9cf815631cc7e779ec134ddd228dc8e9a250e1ea3a910610c59eb8f5c',
                'clang-tools-extra': 'e8d011250389cfc36eb51557ca25ae66ab08173e8d53536a0747356105d72906',
                'lldb': 'e8b948c6c85cd61bd9a48361959401b9c631fa257c0118db26697c5d57460e13',
                'lld': 'f29f684723effd204b6fe96edb1bf2f66f0f81297230bc92b8cc514f7a24236f',
            }
        },
    ]

    # Flang uses its own fork of clang (renamed flang-driver).
    flang_resources = {
        'flang-driver': {
            'git': 'https://github.com/flang-compiler/flang-driver.git',
            'destination': 'tools',
            'placement': 'clang'
        },
        'openmp': {
            'git': 'https://github.com/llvm-mirror/openmp.git',
            'destination': 'projects',
            'placement': 'openmp'
        }
    }

    flang_releases = [
        {
            'version': 'develop',
            'branch': 'release_60',
            'resources': {
                'flang-driver': 'release_60',
                'openmp': 'release_60',
            }
        },
        {
            'version': '20180921',
            'commit': 'd8b30082648dc869eba68f9e539605f437d7760c',
            'resources': {
                'flang-driver': 'dd7587310ae498c22514a33e1a2546b86af9cf25',
                'openmp': 'd5aa29cb3bcf51289d326b4e565613db8aff65ef'
            }
        },
        {
            'version': 'ppc64le-20180921',
            'commit': 'd8b30082648dc869eba68f9e539605f437d7760c',
            'resources': {
                'flang-driver': 'dd7587310ae498c22514a33e1a2546b86af9cf25',
                'openmp': '29b515e1e6d26b5b0d32d47d28dcdb4b8a11470d'
            }
        },
        {
            'version': '20180612',
            'commit': 'f26a3ece4ccd68a52f5aa970ec42837ee0743296',
            'resources': {
                'flang-driver': 'e079fa68cb35a53c88c41a1939f90b94d539e984',
                'openmp': 'd5aa29cb3bcf51289d326b4e565613db8aff65ef'
            }
        },
        {
            'version': 'ppc64le-20180612',
            'commit': '4158932a46eb2f06a166f22a4a52ae48c7d2949e',
            'resources': {
                'flang-driver': '50c1828a134d5a0f1553b355bf0946db48b0aa6d',
                'openmp': '29b515e1e6d26b5b0d32d47d28dcdb4b8a11470d'
            }
        }
    ]

    for release in releases:
        if release['version'] == 'develop':
            version(release['version'], svn=release['repo'])

            for rname, repo in release['resources'].items():
                resource(name=rname,
                         svn=repo,
                         destination=resources[rname]['destination'],
                         when='@%s%s' % (release['version'],
                                         resources[rname].get('variant', "")),
                         placement=resources[rname].get('placement', None))
        else:
            version(release['version'], release['sha256'], url=llvm_url % release)

            for rname, sha256 in release['resources'].items():
                resource(name=rname,
                         url=resources[rname]['url'] % release,
                         sha256=sha256,
                         destination=resources[rname]['destination'],
                         when='@%s%s' % (release['version'],
                                         resources[rname].get('variant', "")),
                         placement=resources[rname].get('placement', None))

    for release in flang_releases:
        if release['version'] == 'develop':
            version('flang-' + release['version'], git=flang_llvm_url, branch=release['branch'])

            for rname, branch in release['resources'].items():
                flang_resource = flang_resources[rname]
                resource(name=rname,
                         git=flang_resource['git'],
                         branch=branch,
                         destination=flang_resource['destination'],
                         placement=flang_resource['placement'],
                         when='@flang-' + release['version'])

        else:
            version('flang-' + release['version'], git=flang_llvm_url, commit=release['commit'])

            for rname, commit in release['resources'].items():
                flang_resource = flang_resources[rname]
                resource(name=rname,
                         git=flang_resource['git'],
                         commit=commit,
                         destination=flang_resource['destination'],
                         placement=flang_resource['placement'],
                         when='@flang-' + release['version'])

    conflicts('+clang_extra', when='~clang')
    conflicts('+lldb',        when='~clang')

    # LLVM 4 and 5 does not build with GCC 8
    conflicts('%gcc@8:',       when='@:5')
    conflicts('%gcc@:5.0.999', when='@8:')

    # OMP TSAN exists in > 5.x
    conflicts('+omp_tsan', when='@:5.99')

    # Github issue #4986
    patch('llvm_gcc7.patch', when='@4.0.0:4.0.1+lldb %gcc@7.0:')
    # Backport from llvm master + additional fix
    # see  https://bugs.llvm.org/show_bug.cgi?id=39696
    # for a bug report about this problem in llvm master.
    patch('constexpr_longdouble.patch', when='@7:8+libcxx')

    @run_before('cmake')
    def check_darwin_lldb_codesign_requirement(self):
        if not self.spec.satisfies('+lldb platform=darwin'):
            return
        codesign = which('codesign')
        mkdir('tmp')
        llvm_check_file = join_path('tmp', 'llvm_check')
        copy('/usr/bin/false', llvm_check_file)

        try:
            codesign('-f', '-s', 'lldb_codesign', '--dryrun',
                     llvm_check_file)

        except ProcessError:
            explanation = ('The "lldb_codesign" identity must be available'
                           ' to build LLVM with LLDB. See https://github.com/'
                           'jevinskie/llvm-lldb/blob/master/docs/code-signing'
                           '.txt for details on how to create this identity.')
            raise RuntimeError(explanation)

    def setup_environment(self, spack_env, run_env):
        spack_env.append_flags('CXXFLAGS', self.compiler.cxx11_flag)

        if '+clang' in self.spec:
            run_env.set('CC', join_path(self.spec.prefix.bin, 'clang'))
            run_env.set('CXX', join_path(self.spec.prefix.bin, 'clang++'))

    def cmake_args(self):
        spec = self.spec
        cmake_args = [
            '-DLLVM_REQUIRES_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_RTTI:BOOL=ON',
            '-DLLVM_ENABLE_EH:BOOL=ON',
            '-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp',
            '-DPYTHON_EXECUTABLE:PATH={0}'.format(spec['python'].command.path),
        ]

        # TODO: Instead of unconditionally disabling CUDA, add a "cuda" variant
        #       (see TODO above), and set the paths if enabled.
        cmake_args.extend([
            '-DCUDA_TOOLKIT_ROOT_DIR:PATH=IGNORE',
            '-DCUDA_SDK_ROOT_DIR:PATH=IGNORE',
            '-DCUDA_NVCC_EXECUTABLE:FILEPATH=IGNORE',
            '-DLIBOMPTARGET_DEP_CUDA_DRIVER_LIBRARIES:STRING=IGNORE'])

        if '+gold' in spec:
            cmake_args.append('-DLLVM_BINUTILS_INCDIR=' +
                              spec['binutils'].prefix.include)
        if '+polly' in spec:
            cmake_args.append('-DLINK_POLLY_INTO_TOOLS:Bool=ON')
        else:
            cmake_args.extend(['-DLLVM_EXTERNAL_POLLY_BUILD:Bool=OFF',
                               '-DLLVM_TOOL_POLLY_BUILD:Bool=OFF',
                               '-DLLVM_POLLY_BUILD:Bool=OFF',
                               '-DLLVM_POLLY_LINK_INTO_TOOLS:Bool=OFF'])

        if '+python' in spec and '+lldb' in spec and spec.satisfies('@5.0.0:'):
            cmake_args.append('-DLLDB_USE_SYSTEM_SIX:Bool=TRUE')
        if '+clang' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_CLANG_BUILD:Bool=OFF')
        if '+lldb' not in spec:
            cmake_args.extend(['-DLLVM_EXTERNAL_LLDB_BUILD:Bool=OFF',
                               '-DLLVM_TOOL_LLDB_BUILD:Bool=OFF'])
        if '+lld' not in spec:
            cmake_args.append('-DLLVM_TOOL_LLD_BUILD:Bool=OFF')
        if '+internal_unwind' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_LIBUNWIND_BUILD:Bool=OFF')
        if '+libcxx' in spec:
            if spec.satisfies('@3.9.0:'):
                cmake_args.append('-DCLANG_DEFAULT_CXX_STDLIB=libc++')
        else:
            cmake_args.append('-DLLVM_EXTERNAL_LIBCXX_BUILD:Bool=OFF')
            cmake_args.append('-DLLVM_EXTERNAL_LIBCXXABI_BUILD:Bool=OFF')
        if '+compiler-rt' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_COMPILER_RT_BUILD:Bool=OFF')

        if '+shared_libs' in spec:
            cmake_args.append('-DBUILD_SHARED_LIBS:Bool=ON')

        if '+link_dylib' in spec:
            cmake_args.append('-DLLVM_LINK_LLVM_DYLIB:Bool=ON')

        if '+all_targets' not in spec:  # all is default on cmake

            targets = ['NVPTX', 'AMDGPU']
            if (spec.version < Version('3.9.0')
                and spec.version[0] != 'flang'):
                # Starting in 3.9.0 CppBackend is no longer a target (see
                # LLVM_ALL_TARGETS in llvm's top-level CMakeLists.txt for
                # the complete list of targets)

                # This also applies to the version of llvm used by flang
                # hence the test to see if the version starts with "flang".
                targets.append('CppBackend')

            if spec.target.family == 'x86' or spec.target.family == 'x86_64':
                targets.append('X86')
            elif spec.target.family == 'arm':
                targets.append('ARM')
            elif spec.target.family == 'aarch64':
                targets.append('AArch64')
            elif (spec.target.family == 'sparc' or
                  spec.target.family == 'sparc64'):
                targets.append('Sparc')
            elif (spec.target.family == 'ppc64' or
                  spec.target.family == 'ppc64le' or
                  spec.target.family == 'ppc' or
                  spec.target.family == 'ppcle'):
                targets.append('PowerPC')

            cmake_args.append(
                '-DLLVM_TARGETS_TO_BUILD:STRING=' + ';'.join(targets))

        if '+omp_tsan' in spec:
            cmake_args.append('-DLIBOMP_TSAN_SUPPORT=ON')

        if self.compiler.name == 'gcc':
            gcc_prefix = ancestor(self.compiler.cc, 2)
            cmake_args.append('-DGCC_INSTALL_PREFIX=' + gcc_prefix)

        if spec.satisfies('@4.0.0:') and spec.satisfies('platform=linux'):
            cmake_args.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')
        return cmake_args

    @run_before('build')
    def pre_install(self):
        with working_dir(self.build_directory):
            # When building shared libraries these need to be installed first
            make('install-LLVMTableGen')
            if self.spec.version >= Version('4.0.0'):
                # LLVMDemangle target was added in 4.0.0
                make('install-LLVMDemangle')
            make('install-LLVMSupport')

    @run_after('install')
    def post_install(self):
        if '+clang' in self.spec and '+python' in self.spec:
            install_tree(
                'tools/clang/bindings/python/clang',
                join_path(site_packages_dir, 'clang'))

        with working_dir(self.build_directory):
            install_tree('bin', join_path(self.prefix, 'libexec', 'llvm'))
