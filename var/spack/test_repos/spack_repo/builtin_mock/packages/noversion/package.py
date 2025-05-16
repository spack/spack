# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from ...build_systems.generic import Package


class Noversion(Package):
    """
    Simple package with no version, which should be rejected since a version
    is required.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    def install(self, spec, prefix):
        touch(join_path(prefix, "an_installation_file"))
