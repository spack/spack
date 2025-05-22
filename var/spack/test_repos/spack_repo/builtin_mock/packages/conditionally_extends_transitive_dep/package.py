# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class ConditionallyExtendsTransitiveDep(Package):
    """Package that tests if the extends directive supports a spec."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    extends("extendee", when="@2:")  # will not satisfy version
    depends_on("extension1")
