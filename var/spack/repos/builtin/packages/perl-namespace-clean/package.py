# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNamespaceClean(PerlPackage):
    """Keep imports and functions out of your namespace."""

    homepage = "https://metacpan.org/pod/namespace::clean"
    url = "https://cpan.metacpan.org/authors/id/R/RI/RIBASUSHI/namespace-clean-0.26_03.tar.gz"

    version("0.27", sha256="8a10a83c3e183dc78f9e7b7aa4d09b47c11fb4e7d3a33b9a12912fd22e31af9d")
    version("0.26_03", sha256="3ad9a1a0ed76eff3be8bcce6ee86b70e9fa372e8ac24ce98f75268827487e396")
    version("0.26_02", sha256="391a55eaaec1af455c5a36445f0d2923f33ebcb8a7d156703c93da2689df8472")
    version("0.26_01", sha256="f3c5b38f7864e703fc66bba4098ea257957f465be0a5de9bd92b6608782db00d")
    version("0.26", sha256="73986e19c4ad0e634e35f4f26e81437f152d8026eb1d91fe795725746ce13eca")
    version("0.25_03", sha256="3666074a7ff48f6e7e18892feee33e1bc3f643752e307e66c2df613a922027e7")
    version("0.25_02", sha256="02cdae96891699e695b945c98219c2be2b14407cfa1cdcd0665184aeaadb645c")
    version("0.25_01", sha256="a047801fbc8158f85a21061440ec613ab15173e33881b8733b137603477ded74")
    version("0.25", sha256="946a2b7b8219562818867ad915cd493637e2639f901db050b835500c8e6ecd04")
    version("0.24", sha256="a661d4484e7de411bc96819aec28805836cfa6a5e276bb3cd346f8e108911230")

    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-b-hooks-endofscope@0.12:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-package-stash@0.23:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
