# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from ...build_systems.generic import Package


class Hwloc(Package):
    version("2.0.3")
