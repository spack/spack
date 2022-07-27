# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParamsUtil(PerlPackage):
    """Simple, compact and correct param-checking functions"""

    homepage = "https://metacpan.org/pod/Params::Util"
    url      = "http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Params-Util-1.07.tar.gz"

    version('1.07', sha256='30f1ec3f2cf9ff66ae96f973333f23c5f558915bb6266881eac7423f52d7c76c')
