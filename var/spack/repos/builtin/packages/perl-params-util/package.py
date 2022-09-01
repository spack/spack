# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParamsUtil(PerlPackage):
    """Simple, compact and correct param-checking functions"""

    homepage = "https://metacpan.org/pod/Params::Util"
    url = "https://cpan.metacpan.org/authors/id/A/AD/ADAMK/Params-Util-1.07.tar.gz"

    version("1.07", sha256="30f1ec3f2cf9ff66ae96f973333f23c5f558915bb6266881eac7423f52d7c76c")
    provides("perl-params-util-pp")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-test-leaktrace", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util@1.18:", type="run")  # AUTO-CPAN2Spack
