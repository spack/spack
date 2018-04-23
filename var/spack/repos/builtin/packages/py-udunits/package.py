##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class PyUdunits(Package):
    """The MetOffice cf_units Python interface to the UDUNITS-2 Library."""
    homepage = "https://github.com/SciTools/cf_units"
    url      = "https://github.com/SciTools/cf_units/archive/v1.1.3.tar.gz"

    version('1.1.3', '8f3a159f43bc407e21b85a9cae04d903')

    maintainers = ['citibeth']

    extends('python')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-netcdf', type=('build', 'run'))
    depends_on('udunits2')

    # See: https://github.com/SciTools/cf_units/blob/master/cf_units/etc/site.cfg.template
    # udunits2_path = /path/to/libudunits2.so
    # udunits2_xml_path = /path/to/udunits2.xml
    site_cfg_template = """[System]
udunits2_path = %s
udunits2_xml_path = %s
"""

    def install(self, spec, prefix):
        setup_py('install', '--prefix=%s' % prefix)

        cfg_template = find_package_file(spec.prefix, 'site.cfg.template')
        cfg = os.path.join(os.path.split(cfg_template)[0], 'site.cfg')

        udunits2_path = os.path.join(
            spec['udunits2'].prefix.lib, 'libudunits2.%s' % dso_suffix)
        udunits2_xml_path = os.path.join(
            spec['udunits2'].prefix, 'share', 'udunits', 'udunits2.xml')

        with open(cfg, 'w') as fout:
            fout.write(
                self.site_cfg_template % (udunits2_path, udunits2_xml_path))


def find_package_file(spack_package_root, name):

    """Finds directory with a specific name, somewhere inside a Spack
    package.

    spack_package_root:
        Root directory to start searching
    oldname:
        Original name of package (not fully qualified, just the leaf)
    newname:
        What to rename it to

    """
    for root, dirs, files in os.walk(spack_package_root):
        path = os.path.join(root, name)

        # Return if we found the file!
        if os.path.isfile(path):
            return path

    return None
