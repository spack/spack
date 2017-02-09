# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
from llnl.util.cpu_name import get_cpu_name
from spack.architecture import Platform, Target
from spack.operating_systems.mac_os import MacOs


class Darwin(Platform):
    priority    = 89

    def __init__(self):
        super(Darwin, self).__init__('darwin')

        # TODO: These are probably overkill
        # Add Intel architectures
        self.add_target('haswell', Target('haswell'))
        self.add_target('broadwell', Target('broadwell'))
        self.add_target('ivybridge', Target('ivybridge'))
        self.add_target('sandybridge', Target('sandybridge'))
        self.add_target('core2', Target('core2'))

        # Add "basic" architectures
        self.add_target('x86_64', Target('x86_64'))
        self.add_target('ppc64le', Target('ppc64le'))
        self.add_target('ppc64', Target('ppc64'))

        # Add IBM architectures
        self.add_target('power7', Target('power7'))
        self.add_target('power8', Target('power8'))
        self.add_target('power8le', Target('power8le'))
        self.add_target('power9', Target('power9'))
        self.add_target('power9le', Target('power9le'))

        self.default = get_cpu_name()
        self.front_end = self.default
        self.back_end = self.default

        if self.default not in self.targets:
            self.add_target(self.default, Target(self.default))

        mac_os = MacOs()

        self.default_os = str(mac_os)
        self.front_os   = str(mac_os)
        self.back_os    = str(mac_os)

        self.add_operating_system(str(mac_os), mac_os)

    @classmethod
    def detect(cls):
        return 'darwin' in platform.system().lower()
