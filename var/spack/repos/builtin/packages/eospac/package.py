##############################################################################
# Copyright (c) 2018, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Eospac(Package):
    """A collection of C routines that can be used to access the Sesame data
       library.
    """

    homepage = "https://laws.lanl.gov/projects/data/eos.html"
    list_url = "https://laws.lanl.gov/projects/data/eos/eospacReleases.php"

    version('6.4.0beta.1_r20171213193219', 'e4e4beabf946f0b8953532832002afc2')
    version('6.3.1_r20161202150449', '549fda008c4169a69b02ec2a9de1e434', preferred=True)

    def url_for_version(self, version):
        return "https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v{0}.tgz".format(version)

    def install(self, spec, prefix):
        with working_dir('Source'):
            make('prefix=%s' % self.spec.prefix, 'install')
