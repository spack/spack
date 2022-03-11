# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class Mujoco(Package):
    """MuJoCo is a physics engine that aims to facilitate research and
    development in robotics, biomechanics, graphics and animation, and
    other areas where fast and accurate simulation is needed. """

    homepage = "https://mujoco.org/"

    mujoco_releases = {
        '2.1.1': {
            'Linux-x86_64':  'd422720fc53f161992b264847d6173eabbe3a3710aa0045d68738ee942f3246e',
        },
        '2.1.0': {
            'Linux-x86_64':  'a436ca2f4144c38b837205635bbd60ffe1162d5b44c87df22232795978d7d012',
            'Darwin-x86_64':  '50226f859d9d3742fa57e1a0a92d656197ec5786f75bfa50ae00eb80fae25e90',
        }
    }

    for ver, packages in mujoco_releases.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg_sha256 = packages.get(key)
        if pkg_sha256:
            version(ver, sha256=pkg_sha256)

    def url_for_version(self, version):

        system_map = {
            'Linux': 'linux',
            'Darwin': 'macos',
        }

        if version == Version('2.1.0'):
            url = "https://mujoco.org/download/mujoco{0}-{1}-x86_64.tar.gz"
            url_version = version.joined
        else:
            url = "https://github.com/deepmind/mujoco/releases/download/{0}/mujoco-{0}-{1}-x86_64.tar.gz"
            url_version = version

        return url.format(url_version, system_map[platform.system()])

    def install(self, spec, prefix):
        copy_tree('.', prefix)

    def setup_run_environment(self, env):
        env.prepend_path('CPATH', prefix.include)
        env.prepend_path('LD_LIBRARY_PATH', prefix.bin)
        if platform.system() == 'Darwin':
            env.prepend_path('DYLD_LIBRARY_PATH', prefix.bin)
