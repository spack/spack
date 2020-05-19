# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ipopt(AutotoolsPackage):
    """Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a
       software package for large-scale nonlinear optimization."""
    homepage = "https://github.com/coin-or/Ipopt"
    url      = "https://github.com/coin-or/Ipopt/archive/releases/3.13.2.tar.gz"

    version('3.13.2',  sha256='891ab9e9c7db29fc8ac5c779ccec6313301098de7bbf735ca230cd5544c49496')
    version('3.13.1',  sha256='64fc63a3fe27cf5efaf17ebee861f7db5bf70aacf9c316c0d37e4beb4eb72e11')
    version('3.13.0',  sha256='dc392396be28c4a0d49bfab399320cb3f70db5b8f090028a883d826a47744ecf')
    version('3.12.13', sha256='ab8b9457dc6c7240a45e74b4a3851821ccafc2927cfa5c8998e95941d67a94d0')
    version('3.12.12', sha256='7587c21f48bc85ae3a84d544fc67cff0d61c41bf2168879f46f7500ee5cabf73')
    version('3.12.11', sha256='d2c402b9e760f8a20314324ff967b8a3dee73d5bcf3739dd8c06a9f2e99da927')
    version('3.12.10', sha256='dfd29dc95ec815e1ff0a3b7dc86ecc8944b24977e40724c35dac25aa192ac3cd')
    version('3.12.9',  sha256='af2b65338d388c9b5528cc3952ecf8d943c46564b6705087d964d0fcdb79a552')
    version('3.12.8',  sha256='fa120112cd3722927f4c9ab3fb7eff9a25638ea28d467874854779a81c7cdde8')
    version('3.12.7',  sha256='f20017c8e880ec1e55d3efbb615209dfe28a58d0ec5147ce9490fe90afe9d445')
    version('3.12.6',  sha256='6e7253705d5c2d1e9bab2dad9f6b0658439cc83f1c51b923aac056bd26bc0f6f')

    variant('coinhsl', default=False,
            description="Build with Coin Harwell Subroutine Libraries")
    variant('metis', default=False,
            description="Build with METIS partitioning support")
    variant('debug', default=False,
            description="Build debug instead of optimized version")

    depends_on("blas")
    depends_on("lapack")
    depends_on("pkgconfig", type='build')
    depends_on("mumps+double~mpi")
    depends_on('coinhsl', when='+coinhsl')
    depends_on('metis@4.0:', when='+metis')

    patch('ipopt_ppc_build.patch', when='arch=ppc64le')
    patch('ipopt_aarch64_build.patch', when='arch=aarch64')

    flag_handler = build_system_flags
    build_directory = 'spack-build'

    # IPOPT does not build correctly in parallel on OS X
    parallel = False

    def configure_args(self):
        spec = self.spec
        # Dependency directories
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix
        mumps_dir = spec['mumps'].prefix

        # Add directory with fake MPI headers in sequential MUMPS
        # install to header search path
        mumps_flags = "-ldmumps -lmumps_common -lpord -lmpiseq"
        mumps_libcmd = "-L%s " % mumps_dir.lib + mumps_flags

        blas_lib = spec['blas'].libs.ld_flags
        lapack_lib = spec['lapack'].libs.ld_flags

        args = [
            "--prefix=%s" % self.prefix,
            "--with-mumps-incdir=%s" % mumps_dir.include,
            "--with-mumps-lib=%s" % mumps_libcmd,
            "--enable-shared",
            "coin_skip_warn_cxxflags=yes",
            "--with-blas-incdir=%s" % blas_dir.include,
            "--with-blas-lib=%s" % blas_lib,
            "--with-lapack-incdir=%s" % lapack_dir.include,
            "--with-lapack-lib=%s" % lapack_lib
        ]

        if 'coinhsl' in spec:
            args.extend([
                '--with-hsl-lib=%s' % spec['coinhsl'].libs.ld_flags,
                '--with-hsl-incdir=%s' % spec['coinhsl'].prefix.include])

        if 'metis' in spec:
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
