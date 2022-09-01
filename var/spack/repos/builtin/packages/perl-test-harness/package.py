# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestHarness(PerlPackage):
    """Contributing to TAP::Harness."""  # AUTO-CPAN2Spack

    homepage = "http://testanything.org/"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/Test-Harness-3.44.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("3.44", sha256="7eb591ea6b499ece6745ff3e80e60cee669f0037f9ccbc4e4511425f593e5297")
    version("3.43_06", sha256="14fdd5b127d64fdc73c1e39c6bdc568370a4773698eaf299ed7c7ab933f75535")

    provides("perl-app-prove")  # AUTO-CPAN2Spack
    provides("perl-app-prove-state")  # AUTO-CPAN2Spack
    provides("perl-app-prove-state-result")  # AUTO-CPAN2Spack
    provides("perl-app-prove-state-result-test")  # AUTO-CPAN2Spack
    provides("perl-tap-base")  # AUTO-CPAN2Spack
    provides("perl-tap-formatter-base")  # AUTO-CPAN2Spack
    provides("perl-tap-formatter-color")  # AUTO-CPAN2Spack
    provides("perl-tap-formatter-console")  # AUTO-CPAN2Spack
    provides("perl-tap-formatter-console-parallelsession")  # AUTO-CPAN2Spack
    provides("perl-tap-formatter-console-session")  # AUTO-CPAN2Spack
    provides("perl-tap-formatter-file")  # AUTO-CPAN2Spack
    provides("perl-tap-formatter-file-session")  # AUTO-CPAN2Spack
    provides("perl-tap-formatter-session")  # AUTO-CPAN2Spack
    provides("perl-tap-harness")  # AUTO-CPAN2Spack
    provides("perl-tap-harness-env")  # AUTO-CPAN2Spack
    provides("perl-tap-object")  # AUTO-CPAN2Spack
    provides("perl-tap-parser")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-aggregator")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-grammar")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-iterator")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-iterator-array")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-iterator-process")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-iterator-stream")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-iteratorfactory")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-multiplexer")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result-bailout")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result-comment")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result-plan")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result-pragma")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result-test")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result-unknown")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result-version")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-result-yaml")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-resultfactory")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-scheduler")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-scheduler-job")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-scheduler-spinner")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-source")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-sourcehandler")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-sourcehandler-executable")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-sourcehandler-file")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-sourcehandler-handle")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-sourcehandler-perl")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-sourcehandler-rawtap")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-yamlish-reader")  # AUTO-CPAN2Spack
    provides("perl-tap-parser-yamlish-writer")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

