# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlYamlTiny(PerlPackage):
    """YAML::Tiny - Read/Write YAML files with as little code as possible"""

    homepage = "https://metacpan.org/pod/YAML::Tiny"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/YAML-Tiny-1.73.tar.gz"

    version("1.73", sha256="bc315fa12e8f1e3ee5e2f430d90b708a5dc7e47c867dba8dce3a6b8fbe257744")
