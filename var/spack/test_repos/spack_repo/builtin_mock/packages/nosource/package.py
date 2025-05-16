# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *

from ...build_systems.generic import Package


class Nosource(Package):
    """Simple package with no source and one dependency"""

    homepage = "http://www.example.com"

    version("1.0")

    depends_on("dependency-install")
