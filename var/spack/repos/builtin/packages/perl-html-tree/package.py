# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHtmlTree(PerlPackage):
    """Work with HTML in a DOM-like tree structure."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/K/KE/KENTNL"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/K/KE/KENTNL/HTML-Tree-5.07.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "5.910-TRIAL", sha256="3f15e318605684c44436a4276e340088edf11f5c5e94f12e3a1ed15602a673d3"
    )  # Pre-release.
    version(
        "5.07",
        sha256="f0374db84731c204b86c1d5b90975fef0d30a86bd9def919343e554e31a9dbbf",
        preferred=True,
    )
    version("5.06", sha256="9c36eb19cbdf9a5906c858948ca51c35bd7561f52cc18c43281acbe57327536e")

    depends_on("perl-module-build", type="build")

    provides("perl-html-assubs")  # AUTO-CPAN2Spack
    provides("perl-html-element")  # AUTO-CPAN2Spack
    provides("perl-html-element-traverse")  # AUTO-CPAN2Spack
    provides("perl-html-parse")  # AUTO-CPAN2Spack
    provides("perl-html-treebuilder")  # AUTO-CPAN2Spack
    #    depends_on("perl-html-formattext", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-lwp-useragent@5.815:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-html-tagset@3.2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-uri-file", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-fatal", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl@5.8:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.28.8:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-test-leaktrace", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-html-parser@3.46:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-html-entities", type="run")  # AUTO-CPAN2Spack

