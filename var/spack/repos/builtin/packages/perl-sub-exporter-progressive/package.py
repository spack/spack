# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSubExporterProgressive(PerlPackage):
    """Progressive Sub::Exporter"""

    homepage = "http://search.cpan.org/~frew/Sub-Exporter-Progressive-0.001013/lib/Sub/Exporter/Progressive.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/F/FR/FREW/Sub-Exporter-Progressive-0.001013.tar.gz"

    version('0.001013', '72cf6acdd2a0a8b105821a4db98e4ebe')
