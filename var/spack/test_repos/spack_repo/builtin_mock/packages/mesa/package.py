# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Mesa(Package):
    """Package depending on libllvm (a link-type virtual provided by a compiler)"""

    homepage = "https://www.mesa.com"

    version("2.0.1")
    depends_on("libllvm")
    depends_on("cxx", type="build")
