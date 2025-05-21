# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin_mock.build_systems.bundle import BundlePackage

from spack.package import *


class NoversionBundle(BundlePackage):
    """
    Simple bundle package with no version and one dependency, which
    should be rejected for lack of a version.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"
    depends_on("dependency-install")
