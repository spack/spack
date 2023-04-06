# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTypeTiny(PerlPackage):
    """Tiny, yet Moo(se)-compatible type constraint."""  # AUTO-CPAN2Spack

    homepage = "https://typetiny.toby.ink/"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Type-Tiny-1.016008.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "1.016.009",
        sha256="69794c37111ae92cd5b36626e6aa914b40b633df136dff7283dffacaf4562e38",
        url="https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Type-Tiny-1.016009.tar.gz",
    )
    version(
        "1.016.008",
        sha256="d554f024d5da0833d623b29a1c0e1aa6147e267266725e9cf322b6d70c60dd0f",
        url="https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Type-Tiny-1.016008.tar.gz",
    )

    provides("perl-devel-typetiny-perl56compat")  # AUTO-CPAN2Spack
    provides("perl-devel-typetiny-perl58compat")  # AUTO-CPAN2Spack
    provides("perl-error-typetiny")  # AUTO-CPAN2Spack
    provides("perl-error-typetiny-assertion")  # AUTO-CPAN2Spack
    provides("perl-error-typetiny-compilation")  # AUTO-CPAN2Spack
    provides("perl-error-typetiny-wrongnumberofparameters")  # AUTO-CPAN2Spack
    provides("perl-eval-typetiny")  # AUTO-CPAN2Spack
    provides("perl-eval-typetiny-codeaccumulator")  # AUTO-CPAN2Spack
    provides("perl-reply-plugin-typetiny")  # AUTO-CPAN2Spack
    provides("perl-test-typetiny")  # AUTO-CPAN2Spack
    provides("perl-type-coercion")  # AUTO-CPAN2Spack
    provides("perl-type-coercion-frommoose")  # AUTO-CPAN2Spack
    provides("perl-type-coercion-union")  # AUTO-CPAN2Spack
    provides("perl-type-library")  # AUTO-CPAN2Spack
    provides("perl-type-params")  # AUTO-CPAN2Spack
    provides("perl-type-params-parameter")  # AUTO-CPAN2Spack
    provides("perl-type-params-signature")  # AUTO-CPAN2Spack
    provides("perl-type-parser")  # AUTO-CPAN2Spack
    provides("perl-type-parser-astbuilder")  # AUTO-CPAN2Spack
    provides("perl-type-parser-token")  # AUTO-CPAN2Spack
    provides("perl-type-parser-tokenstream")  # AUTO-CPAN2Spack
    provides("perl-type-registry")  # AUTO-CPAN2Spack
    provides("perl-type-tiny-class")  # AUTO-CPAN2Spack
    provides("perl-type-tiny-constrainedobject")  # AUTO-CPAN2Spack
    provides("perl-type-tiny-duck")  # AUTO-CPAN2Spack
    provides("perl-type-tiny-enum")  # AUTO-CPAN2Spack
    provides("perl-type-tiny-intersection")  # AUTO-CPAN2Spack
    provides("perl-type-tiny-role")  # AUTO-CPAN2Spack
    provides("perl-type-tiny-union")  # AUTO-CPAN2Spack
    provides("perl-type-utils")  # AUTO-CPAN2Spack
    provides("perl-types-common-numeric")  # AUTO-CPAN2Spack
    provides("perl-types-common-string")  # AUTO-CPAN2Spack
    provides("perl-types-standard")  # AUTO-CPAN2Spack
    provides("perl-types-standard-arrayref")  # AUTO-CPAN2Spack
    provides("perl-types-standard-cycletuple")  # AUTO-CPAN2Spack
    provides("perl-types-standard-dict")  # AUTO-CPAN2Spack
    provides("perl-types-standard-hashref")  # AUTO-CPAN2Spack
    provides("perl-types-standard-map")  # AUTO-CPAN2Spack
    provides("perl-types-standard-scalarref")  # AUTO-CPAN2Spack
    provides("perl-types-standard-strmatch")  # AUTO-CPAN2Spack
    provides("perl-types-standard-tied")  # AUTO-CPAN2Spack
    provides("perl-types-standard-tuple")  # AUTO-CPAN2Spack
    provides("perl-types-typetiny")  # AUTO-CPAN2Spack
    depends_on("perl-ref-util-xs@0.100:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-warnings", type="test")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.17:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-type-tiny-xs@0.16:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.10.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-devel-lexalias@0.5:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-devel-stacktrace", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-sub-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-exporter-tiny@1.0.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-regexp-util@0.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-type-tie", type="run")  # AUTO-CPAN2Spack
