# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlOpen(Package):
    """open - perl pragma to set default PerlIO layers for input and output"""

    homepage = "https://metacpan.org/pod/open"
    url = "https://fastapi.metacpan.org/source/RJBS/perl-5.36.0/lib/open.pm"

    version(
        "5.36",
        sha256="b89b898d8e2014dc7b48d3b186524f82fafcf5b2771dc78815831b1f60ae8415",
        expand=False,
    )

    depends_on("perl")

    def install(self, spec, prefix):
        copy("open.pm", prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("PERL5LIB", self.prefix)
