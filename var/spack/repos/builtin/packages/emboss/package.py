##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class Emboss(AutotoolsPackage):
    """EMBOSS is a free Open Source software analysis package specially
       developed for the needs of the molecular biology (e.g. EMBnet) user
       community"""

    homepage = "http://emboss.sourceforge.net/"
    url      = "ftp://emboss.open-bio.org/pub/EMBOSS/EMBOSS-6.6.0.tar.gz"

    version('6.6.0', 'cc3fca80cb0618deb10fa0d29fe90e4b')

    depends_on('libxpm')
    depends_on('libgd')
    depends_on('postgresql')

    @run_after('configure')
    def skip_update_checks(self):
        # Delete $(bindir)/embossupdate to skip update checks
        filter_file('$(bindir)/embossupdate', '', 'Makefile', string=True)
