# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cmake(Package):
    """A cross-platform, open-source build system. CMake is a family of
       tools designed to build, test and package software."""
    homepage = 'https://www.cmake.org'
    url      = 'https://github.com/Kitware/CMake/releases/download/v3.15.5/cmake-3.15.5.tar.gz'
    maintainers = ['chuckatkins']

    version('3.16.5',   sha256='5f760b50b8ecc9c0c37135fae5fbf00a2fef617059aa9d61c1bb91653e5a8bfc')
    version('3.16.2',   sha256='8c09786ec60ca2be354c29829072c38113de9184f29928eb9da8446a5f2ce6a9')
    version('3.16.1',   sha256='a275b3168fa8626eca4465da7bb159ff07c8c6cb0fb7179be59e12cbdfa725fd')
    version('3.16.0',   sha256='6da56556c63cab6e9a3e1656e8763ed4a841ac9859fefb63cbe79472e67e8c5f')
    version('3.15.5',   sha256='fbdd7cef15c0ced06bb13024bfda0ecc0dedbcaaaa6b8a5d368c75255243beb4')
    version('3.15.4',   sha256='8a211589ea21374e49b25fc1fc170e2d5c7462b795f1b29c84dd0e984301ed7a')
    version('3.15.3',   sha256='13958243a01365b05652fa01b21d40fa834f70a9e30efa69c02604e64f58b8f5')
    version('3.15.2',   sha256='539088cb29a68e6d6a8fba5c00951e5e5b1a92c68fa38a83e1ed2f355933f768')
    version('3.15.1',   sha256='18dec548d8f8b04d53c60f9cedcebaa6762f8425339d1e2c889c383d3ccdd7f7')
    version('3.15.0',   sha256='0678d74a45832cacaea053d85a5685f3ed8352475e6ddf9fcb742ffca00199b5')
    version('3.14.5',   sha256='505ae49ebe3c63c595fa5f814975d8b72848447ee13b6613b0f8b96ebda18c06')
    version('3.14.4',   sha256='00b4dc9b0066079d10f16eed32ec592963a44e7967371d2f5077fd1670ff36d9')
    version('3.14.3',   sha256='215d0b64e81307182b29b63e562edf30b3875b834efdad09b3fcb5a7d2f4b632')
    version('3.14.2',   sha256='a3cbf562b99270c0ff192f692139e98c605f292bfdbc04d70da0309a5358e71e')
    version('3.14.1',   sha256='7321be640406338fc12590609c42b0fae7ea12980855c1be363d25dcd76bb25f')
    version('3.14.0',   sha256='aa76ba67b3c2af1946701f847073f4652af5cbd9f141f221c97af99127e75502')
    version('3.13.4',   sha256='fdd928fee35f472920071d1c7f1a6a2b72c9b25e04f7a37b409349aef3f20e9b')
    version('3.13.3',   sha256='665f905036b1f731a2a16f83fb298b1fb9d0f98c382625d023097151ad016b25')
    version('3.13.2',   sha256='c925e7d2c5ba511a69f43543ed7b4182a7d446c274c7480d0e42cd933076ae25')
    version('3.13.1',   sha256='befe1ce6d672f2881350e94d4e3cc809697dd2c09e5b708b76c1dae74e1b2210')
    version('3.13.0',   sha256='4058b2f1a53c026564e8936698d56c3b352d90df067b195cb749a97a3d273c90')
    version('3.12.4',   sha256='5255584bfd043eb717562cff8942d472f1c0e4679c4941d84baadaa9b28e3194')
    version('3.12.3',   sha256='acbf13af31a741794106b76e5d22448b004a66485fc99f6d7df4d22e99da164a')
    version('3.12.2',   sha256='0f97485799e51a7070cc11494f3e02349b0fc3a24cc12b082e737bf67a0581a4')
    version('3.12.1',   sha256='c53d5c2ce81d7a957ee83e3e635c8cda5dfe20c9d501a4828ee28e1615e57ab2')
    version('3.12.0',   sha256='d0781a90f6cdb9049d104ac16a150f9350b693498b9dea8a0331e799db6b9d69')
    version('3.11.4',   sha256='8f864e9f78917de3e1483e256270daabc4a321741592c5b36af028e72bff87f5')
    version('3.11.3',   sha256='287135b6beb7ffc1ccd02707271080bbf14c21d80c067ae2c0040e5f3508c39a')
    version('3.11.2',   sha256='5ebc22bbcf2b4c7a20c4190d42c084cf38680a85b1a7980a2f1d5b4a52bf5248')
    version('3.11.1',   sha256='57bebc6ca4d1d42c6385249d148d9216087e0fda57a47dc5c858790a70217d0c')
    version('3.11.0',   sha256='c313bee371d4d255be2b4e96fd59b11d58bc550a7c78c021444ae565709a656b')
    version('3.10.3',   sha256='0c3a1dcf0be03e40cf4f341dda79c96ffb6c35ae35f2f911845b72dab3559cf8')
    version('3.10.2',   sha256='80d0faad4ab56de07aa21a7fc692c88c4ce6156d42b0579c6962004a70a3218b')
    version('3.10.1',   sha256='7be36ee24b0f5928251b644d29f5ff268330a916944ef4a75e23ba01e7573284')
    version('3.10.0',   sha256='b3345c17609ea0f039960ef470aa099de9942135990930a57c14575aae884987')
    version('3.9.6',    sha256='7410851a783a41b521214ad987bb534a7e4a65e059651a2514e6ebfc8f46b218')
    version('3.9.4',    sha256='b5d86f12ae0072db520fdbdad67405f799eb728b610ed66043c20a92b4906ca1')
    version('3.9.2',    sha256='954a5801a456ee48e76f01107c9a4961677dd0f3e115275bbd18410dc22ba3c1')
    version('3.9.0',    sha256='167701525183dbb722b9ffe69fb525aa2b81798cf12f5ce1c020c93394dfae0f')
    version('3.8.2',    sha256='da3072794eb4c09f2d782fcee043847b99bb4cf8d4573978d9b2024214d6e92d')
    version('3.8.1',    sha256='ce5d9161396e06501b00e52933783150a87c33080d4bdcef461b5b7fd24ac228')
    version('3.8.0',    sha256='cab99162e648257343a20f61bcd0b287f5e88e36fcb2f1d77959da60b7f35969')
    version('3.7.2',    sha256='dc1246c4e6d168ea4d6e042cfba577c1acd65feea27e56f5ff37df920c30cae0')
    version('3.7.1',    sha256='449a5bce64dbd4d5b9517ebd1a1248ed197add6ad27934478976fd5f1f9330e1')
    version('3.6.1',    sha256='28ee98ec40427d41a45673847db7a905b59ce9243bb866eaf59dce0f58aaef11')
    version('3.6.0',    sha256='fd05ed40cc40ef9ef99fac7b0ece2e0b871858a82feade48546f5d2940147670')
    version('3.5.2',    sha256='92d8410d3d981bb881dfff2aed466da55a58d34c7390d50449aa59b32bb5e62a')
    version('3.5.1',    sha256='93d651a754bcf6f0124669646391dd5774c0fc4d407c384e3ae76ef9a60477e8')
    version('3.5.0',    sha256='92c83ad8a4fd6224cf6319a60b399854f55b38ebe9d297c942408b792b1a9efa')
    version('3.4.3',    sha256='b73f8c1029611df7ed81796bf5ca8ba0ef41c6761132340c73ffe42704f980fa')
    version('3.4.0',    sha256='a5b82bf6ace6c481cdb911fd5d372a302740cbefd387e05297cb37f7468d1cea')
    version('3.3.1',    sha256='cd65022c6a0707f1c7112f99e9c981677fdd5518f7ddfa0f778d4cee7113e3d6')
    version('3.1.0',    sha256='8bdc3fa3f2da81bc10c772a6b64cc9052acc2901d42e1e1b2588b40df224aad9')
    version('3.0.2',    sha256='6b4ea61eadbbd9bec0ccb383c29d1f4496eacc121ef7acf37c7a24777805693e')
    version('2.8.10.2', sha256='ce524fb39da06ee6d47534bbcec6e0b50422e18b62abc4781a4ba72ea2910eb1')

    # Revert the change that introduced a regression when parsing mpi link
    # flags, see: https://gitlab.kitware.com/cmake/cmake/issues/19516
    patch('cmake-revert-findmpi-link-flag-list.patch', when='@3.15.0')

    # Fix linker error when using external libs on darwin.
    # See https://gitlab.kitware.com/cmake/cmake/merge_requests/2873
    patch('cmake-macos-add-coreservices.patch', when='@3.11.0:3.13.3')

    # Fix builds with XLF + Ninja generator
    # https://gitlab.kitware.com/cmake/cmake/merge_requests/4075
    patch('fix-xlf-ninja-mr-4075.patch', sha256="42d8b2163a2f37a745800ec13a96c08a3a20d5e67af51031e51f63313d0dedd1", when="@3.15.5")

    # We default ownlibs to true because it greatly speeds up the CMake
    # build, and CMake is built frequently. Also, CMake is almost always
    # a build dependency, and its libs will not interfere with others in
    # the build.
    variant('ownlibs', default=True,  description='Use CMake-provided third-party libraries')
    variant('qt',      default=False, description='Enables the build of cmake-gui')
    variant('doc',     default=False, description='Enables the generation of html and man page documentation')
    variant('openssl', default=True,  description="Enables CMake's OpenSSL features")
    variant('ncurses', default=True,  description='Enables the build of the ncurses gui')

    # Really this should conflict since it's enabling or disabling openssl for
    # CMake's internal copy of curl.  Ideally we'd want a way to have the
    # openssl variant disabled when ~ownlibs but there's not really a way to
    # tie the values of those togethor, so for now we're just going to ignore
    # the openssl variant entirely when ~ownlibs
    # conflicts('~ownlibs', when='+openssl')

    depends_on('curl',           when='~ownlibs')
    depends_on('expat',          when='~ownlibs')
    depends_on('zlib',           when='~ownlibs')
    depends_on('bzip2',          when='~ownlibs')
    depends_on('xz',             when='~ownlibs')
    depends_on('libarchive@3.1.0:', when='~ownlibs')
    depends_on('libarchive@3.3.3:',     when='@3.15.0:~ownlibs')
    depends_on('libuv@1.0.0:1.10.99',   when='@3.7.0:3.10.3~ownlibs')
    depends_on('libuv@1.10.0:1.10.99',  when='@3.11.0:3.11.99~ownlibs')
    depends_on('libuv@1.10.0:',  when='@3.12.0:~ownlibs')
    depends_on('rhash',          when='@3.8.0:~ownlibs')
    depends_on('qt',             when='+qt')
    depends_on('python@2.7.11:', when='+doc', type='build')
    depends_on('py-sphinx',      when='+doc', type='build')
    depends_on('openssl', when='+openssl')
    depends_on('openssl@:1.0.99', when='@:3.6.9+openssl')
    depends_on('ncurses',        when='+ncurses')

    # Cannot build with Intel, should be fixed in 3.6.2
    # https://gitlab.kitware.com/cmake/cmake/issues/16226
    patch('intel-c-gnu11.patch', when='@3.6.0:3.6.1')

    # https://gitlab.kitware.com/cmake/cmake/issues/18232
    patch('nag-response-files.patch', when='@3.7:3.12')

    conflicts('+qt', when='^qt@5.4.0')  # qt-5.4.0 has broken CMake modules

    # https://gitlab.kitware.com/cmake/cmake/issues/18166
    conflicts('%intel', when='@3.11.0:3.11.4')
    conflicts('%intel@:14', when='@3.14:',
              msg="Intel 14 has immature C++11 support")

    phases = ['bootstrap', 'build', 'install']

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and self.compiler.name == 'fj':
            cxx11plus_flags = (self.compiler.cxx11_flag,
                               self.compiler.cxx14_flag)
            cxxpre11_flags = (self.compiler.cxx98_flag)
            if any(f in flags for f in cxxpre11_flags):
                raise ValueError('cannot build cmake pre-c++11 standard')
            elif not any(f in flags for f in cxx11plus_flags):
                flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)

    def bootstrap_args(self):
        spec = self.spec
        args = [
            '--prefix={0}'.format(self.prefix),
            '--parallel={0}'.format(make_jobs)
        ]

        if '+ownlibs' in spec:
            # Build and link to the CMake-provided third-party libraries
            args.append('--no-system-libs')
        else:
            # Build and link to the Spack-installed third-party libraries
            args.append('--system-libs')

            if spec.satisfies('@3.2:'):
                # jsoncpp requires CMake to build
                # use CMake-provided library to avoid circular dependency
                args.append('--no-system-jsoncpp')

        if '+qt' in spec:
            args.append('--qt-gui')
        else:
            args.append('--no-qt-gui')

        if '+doc' in spec:
            args.append('--sphinx-html')
            args.append('--sphinx-man')

        # Now for CMake arguments to pass after the initial bootstrap
        args.append('--')

        # Make sure to create an optimized release build
        args.append('-DCMAKE_BUILD_TYPE=Release')

        # Install CMake correctly, even if `spack install` runs
        # inside a ctest environment
        args.append('-DCMake_TEST_INSTALL=OFF')

        # When building our own private copy of curl then we need to properly
        # enable / disable oepnssl
        if '+ownlibs' in spec:
            args.append('-DCMAKE_USE_OPENSSL=%s' % str('+openssl' in spec))

        return args

    def bootstrap(self, spec, prefix):
        bootstrap = Executable('./bootstrap')
        bootstrap(*self.bootstrap_args())

    def build(self, spec, prefix):
        make()

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def test(self):
        # Some tests fail, takes forever
        make('test')

    def install(self, spec, prefix):
        make('install')
