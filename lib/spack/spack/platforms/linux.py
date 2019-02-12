# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro


class Linux(Platform):
    priority    = 90

    def __init__(self):
        super(Linux, self).__init__('linux')
        self.add_target('x86_64', Target('x86_64'))
        self.add_target('ppc64le', Target('ppc64le'))

        self.default = platform.machine()
        self.front_end = platform.machine()
        self.back_end = platform.machine()

        if self.default not in self.targets:
            self.add_target(self.default, Target(self.default))

        linux_dist = LinuxDistro()
        self.default_os = str(linux_dist)
        self.front_os = self.default_os
        self.back_os = self.default_os
        self.add_operating_system(str(linux_dist), linux_dist)

    @classmethod
    def detect(cls):
        return 'linux' in platform.system().lower()
