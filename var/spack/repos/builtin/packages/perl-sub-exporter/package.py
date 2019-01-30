# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSubExporter(PerlPackage):
    """A sophisticated exporter for custom-built routines"""

    homepage = "http://search.cpan.org/~rjbs/Sub-Exporter-0.987/lib/Sub/Exporter.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Sub-Exporter-0.987.tar.gz"

    version('0.987', '5332d269a7ba387773fcd140b72a0ed2')

    depends_on('perl-params-util', type=('build', 'run'))
    depends_on('perl-data-optlist', type=('build', 'run'))
