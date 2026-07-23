# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class SimpleResource(Package):
    url = "http://example.com/source-1.0.tgz"

    version("1.0", sha256="1111111111111111111111111111111111111111111111111111111111111111")

    resource(
        name="sample-resource",
        url="https://example.com/resource.tgz",
        checksum="2222222222222222222222222222222222222222222222222222222222222222",
        when="@1.0",
        placement="resource-dst",
        expand="True",
    )
