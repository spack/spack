# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlClassDataInheritable(PerlPackage):
    """For creating accessor/mutators to class data."""

    homepage = "http://search.cpan.org/~tmtm/Class-Data-Inheritable-0.08/lib/Class/Data/Inheritable.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TM/TMTM/Class-Data-Inheritable-0.08.tar.gz"

    version('0.08', 'fc0fe65926eb8fb932743559feb54eb9')
