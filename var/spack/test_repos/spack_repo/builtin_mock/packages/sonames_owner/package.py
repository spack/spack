# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class SonamesOwner(Package):
    """Package detected by its executables, which declares the libraries it owns"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/sonames-owner-1.0.tar.gz"

    executables = ["^sonames-owner$"]
    sonames = [r"^libsonames-owner\.so\.\d+$"]

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    @classmethod
    def determine_version(cls, exe):
        return "1.0"
