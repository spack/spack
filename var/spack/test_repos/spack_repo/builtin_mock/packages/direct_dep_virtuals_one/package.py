# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DirectDepVirtualsOne(Package):
    version("1.0")
    # These two statements imply that %blas=netlib-blas must be false.
    depends_on("direct-dep-virtuals-two +variant", when="%blas=netlib-blas")
    depends_on("direct-dep-virtuals-two ~variant")

    # The provider is a direct dependency, but its virtual is *not* depended on.
    depends_on("netlib-blas")
