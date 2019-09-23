# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.spec import ConflictsInSpecError


class Vdt(CMakePackage):
    """Vectorised math. A collection of fast and inline implementations of
    mathematical functions."""

    homepage = "https://github.com/dpiparo/vdt"
    url      = "https://github.com/dpiparo/vdt/archive/v0.3.9.tar.gz"

    version('0.4.3', sha256='705674612ebb5c182b65a8f61f4d173eb7fe7cdeee2235b402541a492e08ace1')
    version('0.3.9', '80a2d73a82f7ef8257a8206ca22dd145')
    version('0.3.8', '25b07c72510aaa95fffc11e33579061c')
    version('0.3.7', 'd2621d4c489894fd1fe8e056d9a0a67c')
    version('0.3.6', '6eaff3bbbd5175332ccbd66cd71a741d')

    simd_x86 = ('sse', 'avx', 'avx2', 'fma')
    simd_all = ('sse', 'avx', 'avx2', 'fma', 'neon')
    variant(
        'simd',
        default='None',
        values=simd_all,
        description='USE simd instruction set',
        multi=True
    )

    def flag_handler(self, name, flags):
        arch = ''
        spec = self.spec
        if spec.satisfies("platform=cray"):
            # FIXME; It is assumed that cray is x86_64.
            # If you support arm on cray, you need to fix it.
            arch = 'x86_64'
        if arch != 'x86_64' and not spec.satisfies("target=x86_64:"):
            for s in self.simd_x86:
                if (spec.satisfies("simd={0}".format(s))):
                    raise ConflictsInSpecError(
                        spec,
                        [(
                            spec,
                            spec.architecture.target,
                            spec.variants['simd'],
                            'simd=sse,avx,avx2 and fma are valid'
                            ' only on x86_64'
                        )]
                    )
        # FIXME: It is assumed that arm 32 bit target is arm.
        if arch != 'arm' and not spec.satisfies("target=arm"):
            if spec.satisfies("simd=neon"):
                raise ConflictsInSpecError(
                    spec,
                    [(
                        spec,
                        spec.architecture.target,
                        spec.variants['simd'],
                        'simd=neon is valid only on arm 32 bit'
                    )]
                )
        return (flags, None, None)

    @property
    def build_directory(self):
        d = join_path(self.stage.path, 'spack-build')
        if self.spec.satisfies('@:0.3.8'):
            d = self.stage.source_path
        return d

    def cmake_args(self):
        options = []

        for s in self.simd_all:
            options.append(
                "-D{0}=".format(s.upper()) +
                ("ON" if (s in self.spec.variants['simd'].value) else "OFF")
            )
        return options
