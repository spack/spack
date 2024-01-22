# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

import archspec.cpu

import spack.target
from spack.operating_systems.freebsd import FreeBSDOs

from ._platform import Platform


class FreeBSD(Platform):
    priority = 102

    def __init__(self):
        super().__init__("freebsd")

        for name in archspec.cpu.TARGETS:
            self.add_target(name, spack.target.Target(name))

        # Get specific default
        self.default = archspec.cpu.host().name
        self.front_end = self.default
        self.back_end = self.default

        os = FreeBSDOs()
        self.default_os = str(os)
        self.front_os = self.default_os
        self.back_os = self.default_os
        self.add_operating_system(str(os), os)

    @classmethod
    def detect(cls):
        return platform.system().lower() == "freebsd"
