# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPpi(PerlPackage):
    """Parse, Analyze and Manipulate Perl (without perl)."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/Perl-Critic/PPI"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/PPI-1.276.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.276", sha256="657655470e78b7c5b7660f7dec82893489c2e2d880e449135613da3b37500f01")
    version("1.275", sha256="71ef406ce6d0c8ff9545fe308740c958d7892851677ff9c61bb967cd466130d9")

    provides("perl-ppi-cache")  # AUTO-CPAN2Spack
    provides("perl-ppi-document")  # AUTO-CPAN2Spack
    provides("perl-ppi-document-file")  # AUTO-CPAN2Spack
    provides("perl-ppi-document-fragment")  # AUTO-CPAN2Spack
    provides("perl-ppi-document-normalized")  # AUTO-CPAN2Spack
    provides("perl-ppi-dumper")  # AUTO-CPAN2Spack
    provides("perl-ppi-element")  # AUTO-CPAN2Spack
    provides("perl-ppi-exception")  # AUTO-CPAN2Spack
    provides("perl-ppi-exception-parserrejection")  # AUTO-CPAN2Spack
    provides("perl-ppi-find")  # AUTO-CPAN2Spack
    provides("perl-ppi-lexer")  # AUTO-CPAN2Spack
    provides("perl-ppi-node")  # AUTO-CPAN2Spack
    provides("perl-ppi-normal")  # AUTO-CPAN2Spack
    provides("perl-ppi-normal-standard")  # AUTO-CPAN2Spack
    provides("perl-ppi-singletons")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-break")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-compound")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-data")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-end")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-expression")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-given")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-include")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-include-perl6")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-null")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-package")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-scheduled")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-sub")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-unknown")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-unmatchedbrace")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-variable")  # AUTO-CPAN2Spack
    provides("perl-ppi-statement-when")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-block")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-condition")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-constructor")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-for")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-given")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-list")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-subscript")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-unknown")  # AUTO-CPAN2Spack
    provides("perl-ppi-structure-when")  # AUTO-CPAN2Spack
    provides("perl-ppi-token")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-arrayindex")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-attribute")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-bom")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-cast")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-comment")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-dashedword")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-data")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-end")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-heredoc")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-label")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-magic")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-number")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-number-binary")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-number-exp")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-number-float")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-number-hex")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-number-octal")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-number-version")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-operator")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-pod")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-prototype")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quote")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quote-double")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quote-interpolate")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quote-literal")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quote-single")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quotelike")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quotelike-backtick")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quotelike-command")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quotelike-readline")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quotelike-regexp")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-quotelike-words")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-regexp")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-regexp-match")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-regexp-substitute")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-regexp-transliterate")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-separator")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-structure")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-symbol")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-unknown")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-whitespace")  # AUTO-CPAN2Spack
    provides("perl-ppi-token-word")  # AUTO-CPAN2Spack
    provides("perl-ppi-tokenizer")  # AUTO-CPAN2Spack
    provides("perl-ppi-transform")  # AUTO-CPAN2Spack
    provides("perl-ppi-transform-updatecopyright")  # AUTO-CPAN2Spack
    provides("perl-ppi-util")  # AUTO-CPAN2Spack
    provides("perl-ppi-xsaccessor")  # AUTO-CPAN2Spack
    depends_on("perl-test-object@0.7:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-params-util@1.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-class-inspector@1.22:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-clone@0.30:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-task-weaken", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-subcalls@1.7:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-nowarnings", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-digest-md5@2.35:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-util@1.33:", type="run")  # AUTO-CPAN2Spack

