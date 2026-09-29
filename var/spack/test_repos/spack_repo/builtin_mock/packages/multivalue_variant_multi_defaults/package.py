# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class MultivalueVariantMultiDefaults(Package):
    homepage = "http://www.spack.llnl.gov"
    url = "http://www.spack.llnl.gov/mpileaks-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant(
        "myvariant",
        default="bar,baz",
        values=("bar", "baz"),
        multi=True,
        description="Type of libraries to install",
    )

    # conditional dep to incur a cost for packages to build when myvariant includes baz
    depends_on("trivial-install-test-package", when="myvariant=baz")
