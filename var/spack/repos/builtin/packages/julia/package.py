# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.version import ver


def get_best_target(microarch, compiler_name, compiler_version):
    for compiler_entry in microarch.compilers[compiler_name]:
        if compiler_version.satisfies(ver(compiler_entry["versions"])):
            return compiler_entry.get("name", microarch.name)
    raise InstallError("Could not find a target architecture")


class Julia(MakefilePackage):
    """The Julia Language: A fresh approach to technical computing"""

    homepage = "https://julialang.org"
    url      = "https://github.com/JuliaLang/julia/releases/download/v1.7.0/julia-1.7.0.tar.gz"
    git      = "https://github.com/JuliaLang/julia.git"

    maintainers = ['glennpj', 'vchuravy', 'haampie']

    version('master', branch='master')
    version('1.7.2', sha256='0847943dd65001f3322b00c7dc4e12f56e70e98c6b798ccbd4f02d27ce161fef')
    version('1.7.1', sha256='17d298e50e4e3dd897246ccebd9f40ce5b89077fa36217860efaec4576aa718e')
    version('1.7.0', sha256='8e870dbef71bc72469933317a1a18214fd1b4b12f1080784af7b2c56177efcb4')
    version('1.6.5', sha256='b70ae299ff6b63a9e9cbf697147a48a31b4639476d1947cb52e4201e444f23cb')
    version('1.6.4', sha256='a4aa921030250f58015201e28204bff604a007defc5a379a608723e6bb1808d4')

    # We've deprecated these versions, so that we can remove them in Spack 0.18
    # They are still available in Spack 0.17. Julia 0.17.0 is the first version that
    # can be built enitrely from Spack packages, without a network connection during
    # the build.
    for v in [
        '1.6.3', '1.6.2', '1.6.1', '1.6.0', '1.5.4', '1.5.3', '1.5.2', '1.5.1', '1.5.0',
        '1.4.2', '1.4.1', '1.4.0', '1.3.1', '1.2.0', '1.1.1', '1.0.0', '0.6.2', '0.5.2',
        '0.5.1', '0.5.0', '0.4.7', '0.4.6', '0.4.5', '0.4.3'
    ]:
        version(v, deprecated=True)

    variant('precompile', default=True, description='Improve julia startup time')
    variant('openlibm', default=True, description='Use openlibm instead of libm')

    # Note, we just use link_llvm_dylib so that we not only get a libLLVM,
    # but also so that llvm-config --libfiles gives only the dylib. Without
    # it it also gives static libraries, and breaks Julia's build.
    depends_on('llvm targets=amdgpu,bpf,nvptx,webassembly version_suffix=jl +link_llvm_dylib ~internal_unwind')
    depends_on('libuv')

    with when('@1.7.0:1.7'):
        # libssh2.so.1, libpcre2-8.so.0, mbedtls.so.13, mbedcrypto.so.5, mbedx509.so.1
        # openlibm.so.3
        depends_on('libblastrampoline@3.0.0:3')
        depends_on('libgit2@1.1.0:1.1')
        depends_on('libssh2@1.9.0:1.9')
        depends_on('libuv@1.42.0')
        depends_on('llvm@12.0.1')
        depends_on('mbedtls@2.24.0:2.24')
        depends_on('openlibm@0.7.0:0.7', when='+openlibm')

    with when('@1.6.0:1.6'):
        # libssh2.so.1, libpcre2-8.so.0, mbedtls.so.13, mbedcrypto.so.5, mbedx509.so.1
        # openlibm.so.3, (todo: complete this list for upperbounds...)
        depends_on('libgit2@1.1.0:1.1')
        depends_on('libssh2@1.9.0:1.9')
        depends_on('libuv@1.39.0')
        depends_on('llvm@11.0.1')
        depends_on('mbedtls@2.24.0:2.24')
        depends_on('openlibm@0.7.0:0.7', when='+openlibm')

    # Patches for llvm
    depends_on('llvm', patches='llvm7-symver-jlprefix.patch')
    depends_on('llvm', when='^llvm@11.0.1', patches=patch(
        'https://raw.githubusercontent.com/spack/patches/0b543955683a903d711a3e95ff29a4ce3951ca13/julia/llvm-11.0.1-julia-1.6.patch',
        sha256='8866ee0595272b826b72d173301a2e625855e80680a84af837f1ed6db4657f42'))
    depends_on('llvm', when='^llvm@12.0.1', patches=patch(
        'https://github.com/JuliaLang/llvm-project/compare/fed41342a82f5a3a9201819a82bf7a48313e296b...980d2f60a8524c5546397db9e8bbb7d6ea56c1b7.patch',
        sha256='10cb42f80c2eaad3e9c87cb818b6676f1be26737bdf972c77392d71707386aa4'))
    depends_on('llvm', when='^llvm@13.0.0', patches=patch(
        'https://github.com/JuliaLang/llvm-project/compare/d7b669b3a30345cfcdb2fde2af6f48aa4b94845d...6ced34d2b63487a88184c3c468ceda166d10abba.patch',
        sha256='92f022176ab85ded517a9b7aa04df47e19a5def88f291e0c31100128823166c1'))

    # Patches for libuv
    depends_on('libuv', when='^libuv@1.39.0', patches=patch(
        'https://raw.githubusercontent.com/spack/patches/b59ca193423c4c388254f528afabb906b5373162/julia/libuv-1.39.0.patch',
        sha256='f7c1e7341e89dc35dfd85435ba35833beaef575b997c3f978c27d0dbf805149b'))
    depends_on('libuv', when='^libuv@1.42.0', patches=patch(
        'https://raw.githubusercontent.com/spack/patches/89b6d14eb1f3c3d458a06f1e06f7dda3ab67bd38/julia/libuv-1.42.0.patch',
        sha256='d9252fbe67ac8f15e15653f0f6b00dffa07ae1a42f013d4329d17d8b492b7cdb'))

    # patchelf 0.13 is required because the rpath patch uses --add-rpath
    depends_on('patchelf@0.13:', type='build')
    depends_on('perl', type='build')
    depends_on('libwhich', type='build')

    depends_on('blas')  # note: for now openblas is fixed...
    depends_on('curl tls=mbedtls +nghttp2 +libssh2')
    depends_on('dsfmt@2.2.4:')  # apparently 2.2.3->2.2.4 breaks API
    depends_on('gmp')
    depends_on('lapack')  # note: for now openblas is fixed...
    depends_on('libblastrampoline', when='@1.7.0:')
    depends_on('libgit2')
    depends_on('libssh2 crypto=mbedtls')
    depends_on('mbedtls libs=shared')
    depends_on('mpfr')
    depends_on('nghttp2')
    depends_on('openblas +ilp64 symbol_suffix=64_')
    depends_on('openlibm', when='+openlibm')
    depends_on('p7zip')
    depends_on('pcre2')
    depends_on('suite-sparse +pic')
    depends_on('unwind')
    depends_on('utf8proc')
    depends_on('zlib +shared +pic +optimize')

    # Patches for julia
    patch('julia-1.6-system-libwhich-and-p7zip-symlink.patch', when='@1.6.0:1.6')
    patch('use-add-rpath.patch')

    # Fix gfortran abi detection https://github.com/JuliaLang/julia/pull/44026
    patch('fix-gfortran.patch', when='@1.7.0:1.7.1')

    def patch(self):
        # The system-libwhich-libblastrampoline.patch causes a rebuild of docs as it
        # touches the main Makefile, so we reset the a/m-time to doc/_build's.
        f = os.path.join("doc", "_build", "html", "en", "index.html")
        if os.path.exists(f):
            time = (os.path.getatime(f), os.path.getmtime(f))
            os.utime(os.path.join("base", "Makefile"), time)

    def setup_build_environment(self, env):
        # this is a bit ridiculous, but we are setting runtime linker paths to
        # dependencies so that libwhich can locate them.
        if (
            self.spec.satisfies('platform=linux') or
            self.spec.satisfies('platform=cray')
        ):
            linker_var = 'LD_LIBRARY_PATH'
        elif self.spec.satisfies('platform=darwin'):
            linker_var = 'DYLD_FALLBACK_LIBRARY_PATH'
        else:
            return
        pkgs = [
            'curl', 'dsfmt', 'gmp', 'libgit2', 'libssh2', 'libunwind', 'mbedtls',
            'mpfr', 'nghttp2', 'openblas', 'openlibm', 'pcre2', 'suite-sparse',
            'utf8proc', 'zlib'
        ]
        if self.spec.satisfies('@1.7.0:'):
            pkgs.append('libblastrampoline')
        for pkg in pkgs:
            for dir in self.spec[pkg].libs.directories:
                env.prepend_path(linker_var, dir)

    def edit(self, spec, prefix):
        # TODO: use a search query for blas / lapack?
        libblas = os.path.splitext(spec['blas'].libs.basenames[0])[0]
        liblapack = os.path.splitext(spec['lapack'].libs.basenames[0])[0]

        # Host compiler target name
        march = get_best_target(spec.target, spec.compiler.name, spec.compiler.version)

        # LLVM compatible name for the JIT
        julia_cpu_target = get_best_target(spec.target, 'clang', spec['llvm'].version)

        options = [
            'prefix:={0}'.format(prefix),
            'MARCH:={0}'.format(march),
            'JULIA_CPU_TARGET:={0}'.format(julia_cpu_target),
            'USE_BINARYBUILDER:=0',
            'VERBOSE:=1',

            # Spack managed dependencies
            'USE_SYSTEM_BLAS:=1',
            'USE_SYSTEM_CSL:=1',
            'USE_SYSTEM_CURL:=1',
            'USE_SYSTEM_DSFMT:=1',
            'USE_SYSTEM_GMP:=1',
            'USE_SYSTEM_LAPACK:=1',
            'USE_SYSTEM_LIBBLASTRAMPOLINE:=1',
            'USE_SYSTEM_LIBGIT2:=1',
            'USE_SYSTEM_LIBSSH2:=1',
            'USE_SYSTEM_LIBSUITESPARSE:=1',  # @1.7:
            'USE_SYSTEM_SUITESPARSE:=1',  # @:1.6
            'USE_SYSTEM_LIBUNWIND:=1',
            'USE_SYSTEM_LIBUV:=1',
            'USE_SYSTEM_LIBWHICH:=1',
            'USE_SYSTEM_LLVM:=1',
            'USE_SYSTEM_MBEDTLS:=1',
            'USE_SYSTEM_MPFR:=1',
            'USE_SYSTEM_P7ZIP:=1',
            'USE_SYSTEM_PATCHELF:=1',
            'USE_SYSTEM_PCRE:=1',
            'USE_SYSTEM_UTF8PROC:=1',
            'USE_SYSTEM_ZLIB:=1',

            # todo: ilp depends on arch
            'USE_BLAS64:=1',
            'LIBBLASNAME:={0}'.format(libblas),
            'LIBLAPACKNAME:={0}'.format(liblapack),
            'override LIBUV:={0}'.format(spec['libuv'].libs.libraries[0]),
            'override LIBUV_INC:={0}'.format(spec['libuv'].headers.directories[0]),
            'override USE_LLVM_SHLIB:=1',
            # make rebuilds a bit faster for now, not sure if this should be kept
            'JULIA_PRECOMPILE:={0}'.format(
                '1' if spec.variants['precompile'].value else '0'),
        ]

        # libm or openlibm?
        if spec.variants['openlibm'].value:
            options.append('USE_SYSTEM_LIBM=0')
            options.append('USE_SYSTEM_OPENLIBM=1')
        else:
            options.append('USE_SYSTEM_LIBM=1')
            options.append('USE_SYSTEM_OPENLIBM=0')

        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')
