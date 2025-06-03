# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class GmtConcreteMvDependency(Package):
    url = "http://www.example.com/"

    version("2.0", md5="abcdef1234567890abcdef1234567890")
    version("1.0", md5="abcdef1234567890abcdef1234567890")

    depends_on("mvdefaults foo:=a,b")
