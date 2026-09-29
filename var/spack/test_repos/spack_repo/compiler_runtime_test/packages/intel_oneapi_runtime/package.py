# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class IntelOneapiRuntime(Package):
    """Declares a build dependency on the compiler, and a link dependency on gcc-runtime."""

    homepage = "http://www.example.com"
    has_code = False

    tags = ["runtime"]

    # The runtime has a build dependency on the corresponding compiler
    depends_on("intel-oneapi-compilers", type="build")
    # ... and a link dependency on the gcc-runtime corresponding to the gcc used by the compiler
    depends_on("gcc-runtime", type="link")
