# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPpixRegexp(PerlPackage):
    """Parse regular expressions."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/W/WY/WYANT"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/W/WY/WYANT/PPIx-Regexp-0.085.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.085", sha256="2ef0bb89248438e0138fc64c9ab0cacd0a532e908882a07dd8f0b841f130cf1d")
    version("0.084_01", sha256="7bb7e2d62a2118be6a6bcf23fddd1e0515650f8578fdb3204d3279536d58dfae")

    depends_on("perl-module-build", type="build")

    provides("perl-ppix-regexp-constant")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-dumper")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-element")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-lexer")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-node")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-node-range")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-node-unknown")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-assertion")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-atomic-script-run")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-branchreset")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-capture")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-charclass")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-code")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-main")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-modifier")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-namedcapture")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-quantifier")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-regexset")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-regexp")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-replacement")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-script-run")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-subexpression")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-switch")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-structure-unknown")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-support")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-assertion")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-backreference")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-backtrack")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-charclass")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-charclass-posix")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-charclass-posix-unknown")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-charclass-simple")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-code")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-comment")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-condition")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-control")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-delimiter")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-greediness")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-assertion")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-atomic-script-run")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-branchreset")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-code")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-modifier")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-namedcapture")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-script-run")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-subexpression")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-grouptype-switch")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-interpolation")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-literal")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-modifier")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-noop")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-operator")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-quantifier")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-recursion")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-reference")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-structure")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-unknown")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-unmatched")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-token-whitespace")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-tokenizer")  # AUTO-CPAN2Spack
    provides("perl-ppix-regexp-util")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-dumper@1.238:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.42:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-document@1.238:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-task-weaken", type="run")  # AUTO-CPAN2Spack
