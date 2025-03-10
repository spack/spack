# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class AppleVeclib(BundlePackage):
    """Shim package for the core Accelerate vecLib framework from Apple"""
    homepage = "https://developer.apple.com/documentation/accelerate"
    maintainers("elfprince13")

    version("1068.60") # Sequoia 15.3.1

    provides("blas")
    # according to https://developer.apple.com/documentation/accelerate/blas-library
    # there's even a way to get lapack 3.12.0 but start with the bare minimum to get
    # this working
    provides("lapack@3.9.1",when="@1068.60:")

    requires(
        "platform=darwin",
        msg="Apple vecLib is only available on Darwin",
    )

    @property
    def headers(self):
        return HeaderList(
            join_path(self.prefix, "System/Library/Frameworks/Accelerate.framework/Frameworks/vecLib.Framework/Headers")
        )

    @property
    def libs(self):
        return LibraryList(join_path(self.prefix, "System/Library/Frameworks/Accelerate.framework/Frameworks/vecLib.Framework"))
