# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestDeep(PerlPackage):
    """Extremely flexible deep comparison"""

    homepage = "https://metacpan.org/pod/Test::Deep"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Test-Deep-1.127.tar.gz"

    version("1.130", sha256="4064f494f5f62587d0ae501ca439105821ee5846c687dc6503233f55300a7c56")
    version("1.128", sha256="852d7e836fba8269b0b755082051a24a1a309d015a8b76838790af9e3760092f")
    version("1.127", sha256="b78cfc59c41ba91f47281e2c1d2bfc4b3b1b42bfb76b4378bc88cc37b7af7268")

    provides("perl-test-deep-all")  # AUTO-CPAN2Spack
    provides("perl-test-deep-any")  # AUTO-CPAN2Spack
    provides("perl-test-deep-array")  # AUTO-CPAN2Spack
    provides("perl-test-deep-arrayeach")  # AUTO-CPAN2Spack
    provides("perl-test-deep-arrayelementsonly")  # AUTO-CPAN2Spack
    provides("perl-test-deep-arraylength")  # AUTO-CPAN2Spack
    provides("perl-test-deep-arraylengthonly")  # AUTO-CPAN2Spack
    provides("perl-test-deep-blessed")  # AUTO-CPAN2Spack
    provides("perl-test-deep-boolean")  # AUTO-CPAN2Spack
    provides("perl-test-deep-cache")  # AUTO-CPAN2Spack
    provides("perl-test-deep-cache-simple")  # AUTO-CPAN2Spack
    provides("perl-test-deep-class")  # AUTO-CPAN2Spack
    provides("perl-test-deep-cmp")  # AUTO-CPAN2Spack
    provides("perl-test-deep-code")  # AUTO-CPAN2Spack
    provides("perl-test-deep-hash")  # AUTO-CPAN2Spack
    provides("perl-test-deep-hasheach")  # AUTO-CPAN2Spack
    provides("perl-test-deep-hashelements")  # AUTO-CPAN2Spack
    provides("perl-test-deep-hashkeys")  # AUTO-CPAN2Spack
    provides("perl-test-deep-hashkeysonly")  # AUTO-CPAN2Spack
    provides("perl-test-deep-ignore")  # AUTO-CPAN2Spack
    provides("perl-test-deep-isa")  # AUTO-CPAN2Spack
    provides("perl-test-deep-listmethods")  # AUTO-CPAN2Spack
    provides("perl-test-deep-mm")  # AUTO-CPAN2Spack
    provides("perl-test-deep-methods")  # AUTO-CPAN2Spack
    provides("perl-test-deep-notest")  # AUTO-CPAN2Spack
    provides("perl-test-deep-none")  # AUTO-CPAN2Spack
    provides("perl-test-deep-number")  # AUTO-CPAN2Spack
    provides("perl-test-deep-obj")  # AUTO-CPAN2Spack
    provides("perl-test-deep-ref")  # AUTO-CPAN2Spack
    provides("perl-test-deep-reftype")  # AUTO-CPAN2Spack
    provides("perl-test-deep-regexp")  # AUTO-CPAN2Spack
    provides("perl-test-deep-regexpmatches")  # AUTO-CPAN2Spack
    provides("perl-test-deep-regexponly")  # AUTO-CPAN2Spack
    provides("perl-test-deep-regexpref")  # AUTO-CPAN2Spack
    provides("perl-test-deep-regexprefonly")  # AUTO-CPAN2Spack
    provides("perl-test-deep-regexpversion")  # AUTO-CPAN2Spack
    provides("perl-test-deep-scalarref")  # AUTO-CPAN2Spack
    provides("perl-test-deep-scalarrefonly")  # AUTO-CPAN2Spack
    provides("perl-test-deep-set")  # AUTO-CPAN2Spack
    provides("perl-test-deep-shallow")  # AUTO-CPAN2Spack
    provides("perl-test-deep-stack")  # AUTO-CPAN2Spack
    provides("perl-test-deep-string")  # AUTO-CPAN2Spack
    provides("perl-test-deep-subhash")  # AUTO-CPAN2Spack
    provides("perl-test-deep-subhashelements")  # AUTO-CPAN2Spack
    provides("perl-test-deep-subhashkeys")  # AUTO-CPAN2Spack
    provides("perl-test-deep-subhashkeysonly")  # AUTO-CPAN2Spack
    provides("perl-test-deep-superhash")  # AUTO-CPAN2Spack
    provides("perl-test-deep-superhashelements")  # AUTO-CPAN2Spack
    provides("perl-test-deep-superhashkeys")  # AUTO-CPAN2Spack
    provides("perl-test-deep-superhashkeysonly")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util@1.9:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-util@1.9:", type="run")  # AUTO-CPAN2Spack
