# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DropPatch(Package):
    version("1.0")
    patch(
        "https://myrepo.com/patch1.patch",
        sha256="abc",
        when="@1.0",
    )
    patch(
        "https://myrepo.com/patch2.patch",
        sha256="def",
        when="@1.0",
    )
    drop_patch(
        "https://myrepo.com/patch2.patch",
        sha256="def",
        when="@1.0",
    )