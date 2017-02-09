# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro
from llnl.util.cpu_name import get_cpu_name

class Linux(Platform):
    priority    = 90

    def __init__(self):
        super(Linux, self).__init__('linux')

        # Add "basic" architectures
        self.add_target('x86_64', Target('x86_64'))
        self.add_target('ppc64le', Target('ppc64le'))
        self.add_target('ppc64', Target('ppc64'))

        # Add Intel architectures
        self.add_target('haswell', Target('haswell'))
        self.add_target('broadwell', Target('broadwell'))
        self.add_target('ivybridge', Target('ivybridge'))
        self.add_target('sandybridge', Target('sandybridge'))
        self.add_target('knl', Target('knl'))

        # Add IBM architectures
        self.add_target('power7', Target('power7'))
        self.add_target('power8', Target('power8'))
        self.add_target('power8le', Target('power8le'))
        self.add_target('power9', Target('power9'))
        self.add_target('power9le', Target('power9le'))
        # Eternal TODO: Add more architectures as needed.

        # Get specific default
        self.default = get_cpu_name()
        self.front_end = self.default
        self.back_end = self.default

        if not self.default:
            # Fall back on more general name.
            # This will likely fall in "basic" architectures list
            self.default = platform.machine()
            self.front_end = self.default
            self.back_end = self.default

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
