# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Externaltool(Package):
    homepage = "http://somewhere.com"
    has_code = False

    version("1.0")
    version("0.9")
    version("0.8.1")

    depends_on("externalprereq")
