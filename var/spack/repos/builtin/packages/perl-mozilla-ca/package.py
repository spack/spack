# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlMozillaCa(PerlPackage):
    """Mozilla's CA cert bundle in PEM format"""

    homepage = "http://search.cpan.org/~abh/Mozilla-CA-20160104/lib/Mozilla/CA.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/A/AB/ABH/Mozilla-CA-20160104.tar.gz"

    version('20160104', '1b91edb15953a8188f011ab5ff433300')
