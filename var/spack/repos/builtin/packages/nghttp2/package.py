# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os


class Nghttp2(AutotoolsPackage):
    """nghttp2 is an implementation of HTTP/2 and its header compression
       algorithm HPACK in C."""

    homepage = "https://nghttp2.org/"
    url      = "https://github.com/nghttp2/nghttp2/releases/download/v1.26.0/nghttp2-1.26.0.tar.gz"

    version('1.43.0', sha256='45cc3ed91966551f92b31958ceca9b3a9f23ce4faf5cbedb78aa3327cd4e5907')
    version('1.42.0', sha256='884d18a0158908125d58b1b61d475c0325e5a004e3d61a56b5fcc55d5f4b7af5')
    version('1.41.0', sha256='eacc6f0f8543583ecd659faf0a3f906ed03826f1d4157b536b4b385fe47c5bb8')
    version('1.40.0', sha256='eb9d9046495a49dd40c7ef5d6c9907b51e5a6b320ea6e2add11eb8b52c982c47')
    version('1.39.2', sha256='fc820a305e2f410fade1a3260f09229f15c0494fc089b0100312cd64a33a38c0')
    version('1.39.1', sha256='25b623cd04dc6a863ca3b34ed6247844effe1aa5458229590b3f56a6d53cd692')
    version('1.39.0', sha256='6eeb0ccde2dfc5ff8b13c8ce448d944d4402de9c265ab6b98c8129538728aa75')
    version('1.38.0', sha256='fe9a75ec44e3a2e8f7f0cb83ad91e663bbc4c5085baf37b57ee2610846d7cf5d')
    version('1.37.0', sha256='760981ab5703d3ed185eccb322321d379453974357a3263971a928c2879a43bf')
    version('1.36.0', sha256='6b222a264aca23d497f7878a7751bd9da12676717493fe747db49afb51daae79')
    version('1.26.0', sha256='daf7c0ca363efa25b2cbb1e4bd925ac4287b664c3d1465f6a390359daa3f0cf1')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-cython@0.19:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))

    def setup_build_environment(self, env):
        site_packages_dir = os.path.join(
            self.spec.prefix.lib,
            'python' + str(self.spec['python'].version.up_to(2)),
            'site-packages')
        env.prepend_path('PYTHONPATH', site_packages_dir)

    @run_before('install')
    def ensure_install_dir_exists(self):
        site_packages_dir = os.path.join(
            self.spec.prefix.lib,
            'python' + str(self.spec['python'].version.up_to(2)),
            'site-packages')
        mkdirp(site_packages_dir)
