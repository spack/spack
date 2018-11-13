# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nghttp2(AutotoolsPackage):
    """nghttp2 is an implementation of HTTP/2 and its header compression
       algorithm HPACK in C."""

    homepage = "https://nghttp2.org/"
    url      = "https://github.com/nghttp2/nghttp2/releases/download/v1.26.0/nghttp2-1.26.0.tar.gz"

    version('1.26.0', '83fa813b22bacbc6ea80dfb24847569f')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-cython@0.19:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))

    def setup_environment(self, spack_env, run_env):
        site_packages_dir = '/'.join(
            [self.spec.prefix.lib,
             ('python' + str(self.spec['python'].version.up_to(2))),
             'site-packages'])
        spack_env.prepend_path('PYTHONPATH', site_packages_dir)

    @run_before('install')
    def ensure_install_dir_exists(self):
        site_packages_dir = '/'.join(
            [self.spec.prefix.lib,
             ('python' + str(self.spec['python'].version.up_to(2))),
             'site-packages'])
        mkdirp(site_packages_dir)
