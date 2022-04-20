# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ipopt(AutotoolsPackage):
    """Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a
       software package for large-scale nonlinear optimization."""

    homepage = "https://github.com/coin-or/Ipopt"
    url      = "https://www.coin-or.org/download/source/Ipopt/Ipopt-3.13.2.tgz"
    maintainers = ['goxberry']
    # Alternative: url      = "https://github.com/coin-or/Ipopt/archive/releases/3.13.2.tar.gz"

    version('3.14.4', sha256='60865150b6fad19c5968395b57ff4a0892380125646c3afa2a714926f5ac9487')
    version('3.14.3', sha256='29bbf8bbadd5f2965e18e33451723d1fed0c42b14f6493396cf53a05cdfd2c09')
    version('3.14.2', sha256='3ec6776b9a1ed8895f662bfc9939b067722770297be78ca4d6dc1cb42557da62')
    version('3.14.1', sha256='afa37bbb0d91003c58284113717dc304718a1f236c97fe097dfab1672cb879c6')
    version('3.14.0',  sha256='9bed72a5456ef37f1b95746c932986e6664eb70b983d4fab61cf8aa811facdf1')
    version('3.13.4',  sha256='1fdd0f8ea637856d66b1ebdd7d52ad1b8b8c1142d1a4ce0976b200ab280e5683')
    version('3.13.3',  sha256='86354b36c691e6cd6b8049218519923ab0ce8a6f0a432c2c0de605191f2d4a1c')
    version('3.13.2',  sha256='891ab9e9c7db29fc8ac5c779ccec6313301098de7bbf735ca230cd5544c49496')
    version('3.13.1',  sha256='64fc63a3fe27cf5efaf17ebee861f7db5bf70aacf9c316c0d37e4beb4eb72e11')
    version('3.13.0',  sha256='dc392396be28c4a0d49bfab399320cb3f70db5b8f090028a883d826a47744ecf')
    version('3.12.13', sha256='aac9bb4d8a257fdfacc54ff3f1cbfdf6e2d61fb0cf395749e3b0c0664d3e7e96')
    version('3.12.12', sha256='7baeb713ef8d1999bed397b938e9654b38ad536406634384455372dd7e4ed61f')
    version('3.12.11', sha256='cbfc8a37978fdbaeed73b5b2d93b92b7c8b5b615ece02d4646e1556b0a7b382a')
    version('3.12.10', sha256='e1a3ad09e41edbfe41948555ece0bdc78757a5ca764b6be5a9a127af2e202d2e')
    version('3.12.9',  sha256='8ff3fe1a8560896fc5559839a87c2530cac4ed231b0806e487bfd3cf2d294ab8')
    version('3.12.8',  sha256='62c6de314220851b8f4d6898b9ae8cf0a8f1e96b68429be1161f8550bb7ddb03')
    version('3.12.7',  sha256='9c8b02149fa4f0cdf63e838ae68f86aa41a577d7f05932139eede9179f314861')
    version('3.12.6',  sha256='6aaa6bd862d54eba6fb966950fa6928ca01d66cf4cb842b2f41a7ebfa61eee2b')
    version('3.12.5',  sha256='53e7af6eefcb6de1f8e936c9c887c7bcb5a9fa4fcf7673a227f16de131147325')
    version('3.12.4',  sha256='292afd952c25ec9fe6225041683dcbd3cb76e15a128764671927dbaf881c2e89')
    version('3.12.3',  sha256='754fb9473bc683b59a53d2057ff852d0a8d56198bcdba2e2529ce299243fdaa5')
    version('3.12.2',  sha256='3903657788bff7d7743f8bb25c34ccf91c445e72a4710cb821c024107bd1b474')
    version('3.12.1',  sha256='d6c18f7c5bf486712b493167d27ec6e940ad376c5b903b97acc5a3ade1c0a3ef')
    version('3.12.0',  sha256='ed19e5e7174355e93c93c798b5056036e2fd2ec78cf0f3954876483f74fe618b')

    def url_for_version(self, version):
        if version >= Version('3.13.4'):
            return "https://www.coin-or.org/download/source/Ipopt/Ipopt-{0}.tar.gz".format(version)
        else:
            return "https://www.coin-or.org/download/source/Ipopt/Ipopt-{0}.tgz".format(version)

    variant('coinhsl', default=False,
            description="Build with Coin Harwell Subroutine Libraries")
    variant('metis', default=False,
            description="Build with METIS partitioning support")
    variant('debug', default=False,
            description="Build debug instead of optimized version")
    variant('mumps', default=True,
            description='Build with support for linear solver MUMPS')

    depends_on("blas")
    depends_on("lapack")
    depends_on("pkgconfig", type='build')
    depends_on("mumps+double~mpi", when='+mumps')
    depends_on('coinhsl', when='+coinhsl')
    depends_on('metis@4.0:', when='+metis')

    # Must have at least one linear solver available!
    conflicts('~mumps', when='~coinhsl')

    patch('ipopt_ppc_build.patch', when='arch=ppc64le')

    flag_handler = build_system_flags
    build_directory = 'spack-build'

    # IPOPT does not build correctly in parallel on OS X
    parallel = False

    def configure_args(self):
        spec = self.spec
        # Dependency directories
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix

        blas_lib = spec['blas'].libs.ld_flags
        lapack_lib = spec['lapack'].libs.ld_flags

        args = [
            "--prefix=%s" % self.prefix,
            "--enable-shared",
            "coin_skip_warn_cxxflags=yes",
        ]

        if spec.satisfies('@:3.12.13'):
            args.extend([
                "--with-lapack-lib={0}".format(lapack_lib),
                "--with-lapack-incdir={0}".format(lapack_dir.include),
                "--with-blas-lib={0}".format(blas_lib),
                "--with-blas-incdir={0}".format(blas_dir.include),
            ])
        else:
            args.extend([
                "--with-lapack-lflags={0} {1}".format(lapack_lib, blas_lib),
            ])

        if '+mumps' in spec:
            mumps_dir = spec['mumps'].prefix
            mumps_flags = "-ldmumps -lmumps_common -lpord -lmpiseq"
            mumps_libcmd = "-L%s " % mumps_dir.lib + mumps_flags
            if spec.satisfies('@:3.12.13'):
                args.extend([
                    "--with-mumps-incdir=%s" % mumps_dir.include,
                    "--with-mumps-lib=%s" % mumps_libcmd])
            else:
                args.extend([
                    "--with-mumps",
                    "--with-mumps-lflags=%s" % mumps_libcmd,
                    "--with-mumps-cflags=%s" % mumps_dir.include])

        if 'coinhsl' in spec:
            if spec.satisfies('@:3.12.13'):
                args.extend([
                    '--with-hsl-lib=%s' % spec['coinhsl'].libs.ld_flags,
                    '--with-hsl-incdir=%s' % spec['coinhsl'].prefix.include])
            else:
                args.extend([
                    "--with-hsl",
                    "--with-hsl-lflags=%s" % spec['coinhsl'].libs.ld_flags,
                    "--with-hsl-cflags=%s" % spec['coinhsl'].prefix.include])

        if 'metis' in spec:
            if spec.satisfies('@:3.12.13'):
                args.extend([
                    '--with-metis-lib=%s' % spec['metis'].libs.ld_flags,
                    '--with-metis-incdir=%s' % spec['metis'].prefix.include])

        # The IPOPT configure file states that '--enable-debug' implies
        # '--disable-shared', but adding '--enable-shared' overrides
        # '--disable-shared' and builds a shared library with debug symbols
        if '+debug' in spec:
            args.append('--enable-debug')
        else:
            args.append('--disable-debug')

        return args
