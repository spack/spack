# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

from spack.operating_systems.freebsd import FreeBSDOs

from ._platform import Platform, PlatformSupport


class FreeBSD(Platform):
    priority = 102

    platform_support = PlatformSupport.FREEBSD

    def __init__(self):
        super().__init__("freebsd")
        os = FreeBSDOs()
        self.default_os = str(os)
        self.add_operating_system(str(os), os)

    @classmethod
    def detect(cls):
        return platform.system().lower() == "freebsd"
