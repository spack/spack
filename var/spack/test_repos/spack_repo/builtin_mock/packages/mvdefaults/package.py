# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Mvdefaults(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/mvdefaults-1.0.tar.gz"

    version("1.0", md5="abcdef1234567890abcdef1234567890")
    version("0.9", md5="abcdef1234567890abcdef1234567890")

    variant("foo", values=("a", "b", "c"), default=("a", "b", "c"), multi=True, description="")
    conflicts("foo:=a,b", when="@0.9")

    depends_on("pkg-b", when="foo:=b,c")
