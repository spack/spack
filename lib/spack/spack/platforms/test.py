# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.architecture import Platform, Target
from spack.architecture import OperatingSystem


class Test(Platform):
    priority    = 1000000
    front_end   = 'x86'
    back_end    = 'x86_64'
    default     = 'x86_64'

    front_os = 'redhat6'
    back_os = 'debian6'
    default_os = 'debian6'

    def __init__(self):
        super(Test, self).__init__('test')
        self.add_target(self.default, Target(self.default))
        self.add_target(self.front_end, Target(self.front_end))

        self.add_operating_system(
            self.default_os, OperatingSystem('debian', 6))
        self.add_operating_system(
            self.front_os, OperatingSystem('redhat', 6))

    @classmethod
    def detect(cls):
        return True
