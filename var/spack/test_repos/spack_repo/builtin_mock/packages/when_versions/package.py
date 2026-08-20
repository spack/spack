# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class WhenVersions(Package):
    """Package that tests when= for versions()."""

    homepage = "http://www.example.com"

    version("1.0", url="http://www.example.com/linux", when="platform=linux")
    version("1.0", url="http://www.example.com/darwin", when="platform=darwin")
    # Test backwards compatability
    version("2.0",  url="http://www.example.com/")
