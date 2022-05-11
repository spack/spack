# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PerlClassLoad(PerlPackage):
    """A working (require "Class::Name") and more"""

    homepage = "https://metacpan.org/pod/Class::Load"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Class-Load-0.24.tar.gz"

    version('0.24', sha256='0bb983da46c146534fc77a556d6e40d925142f2eb43103534025ee545265ca36')
