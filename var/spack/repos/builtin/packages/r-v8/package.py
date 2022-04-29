# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RV8(RPackage):
    """Embedded JavaScript and WebAssembly Engine for R.

    An R interface to V8: Google's open source JavaScript and WebAssembly
    engine. This package can be compiled either with V8 version 6 and up or
    NodeJS when built as a shared library."""

    cran = "V8"

    version('4.0.0', sha256='146a4cb671264f865ac2f2e35bfdfb37e2df70e4f6784354fb6e8a80a19dbbc8')
    version('3.6.0', sha256='a3969898bf4a7c13d3130fae0d385cd048d46372ff4a412917b914b159261377')
    version('3.4.0', sha256='f5c8a2a03cc1be9f504f47711a0fcd1b962745139c9fb2a10fbd79c4ae103fbd',
            deprecated=True)

    depends_on('r-rcpp@0.12.12:', type=('build', 'run'))
    depends_on('r-jsonlite@1.0:', type=('build', 'run'))
    depends_on('r-curl@1.0:', type=('build', 'run'))

    conflicts('@3.4.0', when='target=aarch64:')
    conflicts('@3.4.0', when='%gcc@5:')

    def setup_build_environment(self, env):
        spec = self.spec
        if ((spec.platform == 'darwin') or
            (spec.platform == 'linux' and spec.target.family == 'x86_64')):
            env.append_flags('DOWNLOAD_STATIC_LIBV8', '1')
