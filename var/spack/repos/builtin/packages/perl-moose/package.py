##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PerlMoose(PerlPackage):
    """A postmodern object system for Perl 5"""

    homepage = "http://search.cpan.org/~ether/Moose-2.2006/lib/Moose.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Moose-2.2006.tar.gz"

    version('2.2006', '929c6b3877a6054ef617cf7ef1e220b5')

    depends_on('perl-cpan-meta-check', type=('build', 'run'))
    depends_on('perl-test-cleannamespaces', type=('build', 'run'))
    depends_on('perl-devel-overloadinfo', type=('build', 'run'))
    depends_on('perl-class-load-xs', type=('build', 'run'))
    depends_on('perl-devel-stacktrace', type=('build', 'run'))
    depends_on('perl-eval-closure', type=('build', 'run'))
    depends_on('perl-sub-name', type=('build', 'run'))
    depends_on('perl-module-runtime-conflicts', type=('build', 'run'))
    depends_on('perl-devel-globaldestruction', type=('build', 'run'))
    depends_on('perl-package-deprecationmanager', type=('build', 'run'))
    depends_on('perl-package-stash-xs', type=('build', 'run'))
