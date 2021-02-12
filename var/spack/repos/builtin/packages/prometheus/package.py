# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Prometheus(MakefilePackage):
    """Prometheus, a Cloud Native Computing Foundation project, is a
    systems and service monitoring system."""

    homepage = "https://prometheus.io/"
    url      = "https://github.com/prometheus/prometheus/archive/v2.19.2.tar.gz"

    version('2.24.1', sha256='434f6931705d9e57f40b696e023a95b7e65c5ca572ad8c0af81f99b3332ae107')
    version('2.24.0', sha256='df74b5abbf78b4b5f194b67c9696e7c2974ae1288ecaac345838cfa668406be4')
    version('2.23.0', sha256='303aa700151884158a2254e26a2808a38eb09d557c6a8f06331d60852f06bdfc')
    version('2.22.2', sha256='99402be6f1c6f1905c6331af520ddfac2863560f7c9978bea68149c48a543012')
    version('2.22.1', sha256='ef6b4983b5c44ab31823fa9dc392135c1bb2c49e271ac282a458368ef6cbf55b')
    version('2.22.0', sha256='234b86f57d0caae4645e2252c7265b39c523b0af24ce64f7bf7c1ba0f347da34')
    version('2.19.2', sha256='d4e84cae2fed6761bb8a80fcc69b6e0e9f274d19dffc0f38fb5845f11da1bbc3')
    version('2.19.1', sha256='b72b9b6bdbae246dcc29ef354d429425eb3c0a6e1596fc8b29b502578a4ce045')
    version('2.18.2', sha256='a26c106c97d81506e3a20699145c11ea2cce936427a0e96eb2fd0dc7cd1945ba')
    version('2.17.1', sha256='d0b53411ea0295c608634ca7ef1d43fa0f5559e7ad50705bf4d64d052e33ddaf')
    version('2.17.0', sha256='b5e508f1c747aaf50dd90a48e5e2a3117fec2e9702d0b1c7f97408b87a073009')

    depends_on('go', type='build')
    depends_on('node-js@11.10.1:', type='build')
    depends_on('yarn', type='build')

    def build(self, spec, prefix):
        make('build', parallel=False)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('prometheus', prefix.bin)
        install('promtool', prefix.bin)
        install('tsdb/tsdb', prefix.bin)
        install_tree('documentation', prefix.documentation)
