# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlTryTinyRetry(PerlPackage):
    """Extends Try::Tiny to allow for retrying a block of code several times before failing"""

    homepage = "https://metacpan.org/pod/Try::Tiny::Retry"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Try-Tiny-Retry-0.004.tar.gz"

    license("Apache-2.0", checked_by="caelanjmiller")

    version("0.004", sha256="8af70c1bd46d749388738b7ea03c703cac898be939a5ff37117a01ed7eda8bbe")
    version("0.003", sha256="6367bf56aa129b7b240b330bd106941fc8c3c22b85fd77ca106aa2778b441e32")
    version("0.002", sha256="4f6dd3addcab7dd2726f450cecaaadb21b33da59bec5df58f07fd91a87d9c38a")
    version("0.001", sha256="a09589bf8b78e5666e12009b0eba0212fb5f89f3d1ab78c0f16050badf69d9c7")

    depends_on("perl-carp", type=("build", "run"))
    depends_on("perl-exporter-tiny", type=("build", "run"))
    depends_on("perl-time-hires", type=("build", "run"))
    depends_on("perl-try-tiny", type=("build", "run"))
