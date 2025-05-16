# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

from ...build_systems.generic import Package


class PkgB(Package):
    homepage = "http://www.example.com"
    has_code = False

    version("1.0")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
