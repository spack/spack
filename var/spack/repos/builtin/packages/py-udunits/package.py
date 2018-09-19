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
import os


class PyUdunits(PythonPackage):
    """The MetOffice cf_units Python interface to the UDUNITS-2 Library."""
    homepage = "https://github.com/SciTools/cf_units"
    url      = "https://github.com/SciTools/cf_units/archive/v1.1.3.tar.gz"

    version('1.1.3', '61ea2239c87b4c1d5d30147800a9e750')

    maintainers = ['citibeth']

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('udunits2')

    # See: https://github.com/SciTools/cf_units/blob/master/cf_units/etc/site.cfg.template
    # udunits2_path = /path/to/libudunits2.so
    # udunits2_xml_path = /path/to/udunits2.xml
    site_cfg_template = """[System]
udunits2_path = %s
udunits2_xml_path = %s
"""

    @run_after('install')
    def configure_template(self):
        spec = self.spec

        cfg_templates = find(spec.prefix, ['site.cfg.template'])
        if len(cfg_templates) != 1:
            tty.die(
                'Found %d instances of site.cfg.template, wanted 1' %
                len(cfg_templates))
        cfg_template = cfg_templates[0]

        cfg = os.path.join(os.path.split(cfg_template)[0], 'site.cfg')

        udunits2_xml_path = os.path.join(
            spec['udunits2'].prefix, 'share', 'udunits', 'udunits2.xml')

        with open(cfg, 'w') as fout:
            fout.write(self.site_cfg_template %
                       (spec['udunits2'].libs, udunits2_xml_path))
