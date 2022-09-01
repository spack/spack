# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHtmlFormatter(PerlPackage):
    """Base class for HTML formatters."""  # AUTO-CPAN2Spack

    homepage = "https://metacpan.org/release/HTML-Formatter"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/N/NI/NIGELM/HTML-Formatter-2.16.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("2.16", sha256="cb0a0dd8aa5e8ba9ca214ce451bf4df33aa09c13e907e8d3082ddafeb30151cc")
    version("2.14", sha256="d28eeeab48ab5f7bfcc73cc106b0f756073d98d48dfdb91ca2951f832f8e035e")

    depends_on("perl-html-element@3.15:", type=("build", "test"))
    provides("perl-html-formatmarkdown")  # AUTO-CPAN2Spack
    provides("perl-html-formatps")  # AUTO-CPAN2Spack
    provides("perl-html-formatrtf")  # AUTO-CPAN2Spack
    provides("perl-html-formattext")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-timesbolditalic", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-warnings", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-helvetica", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-timesroman", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-html-element@3.15:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-courieroblique", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-helveticaoblique", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-courierboldoblique", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-timesbold", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-helveticabold", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-timesitalic", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-courier", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-file-slurper", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-courierbold", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-font-metrics-helveticaboldoblique", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-html-treebuilder", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type="run")  # AUTO-CPAN2Spack

