# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import PackageBase, version


class FailTestAuditBuilder(PackageBase):
    """This package inherits from PackageBase but not a GenericPackage or
    Package."""

    homepage = "http://github.com/dummy/fail-test-audit-builder"
    url = "https://github.com/dummy/fail-test-audit-builder/archive/v1.0.tar.gz"

    version("1.0", sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234")
