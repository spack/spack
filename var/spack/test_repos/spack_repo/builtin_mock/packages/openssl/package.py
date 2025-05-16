# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from ...build_systems.generic import Package


class Openssl(Package):
    version("3.4.0")
