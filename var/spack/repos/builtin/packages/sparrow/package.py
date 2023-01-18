# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sparrow(Package):
    """Sparrow: fast semiempirical quantum chemical calculations."""

    homepage = "https://scine.ethz.ch/download/sparrow"
    url = "https://github.com/qcscine/sparrow/archive/refs/tags/3.0.0.tar.gz"

    version(
        "3.0.0",
        "70636871694c9363ae3fb2df5050bddb22667b71d875d5a7e9afd872f6a2b65d",
        deprecated=True,  # Package renamed to scine-sparrow
    )

    # Original package would always provide Python bindings
    depends_on("scine-sparrow+python@3.0.0")

    def install(self, spec, prefix):
        touch(join_path(prefix, "stub"))
