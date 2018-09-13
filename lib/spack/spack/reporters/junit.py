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
import os
import os.path

import spack.build_environment
import spack.fetch_strategy
import spack.package
from spack.reporter import Reporter

__all__ = ['JUnit']


class JUnit(Reporter):
    """Generate reports of spec installations for JUnit."""

    def __init__(self, install_command, cdash_upload_url):
        Reporter.__init__(self, install_command, cdash_upload_url)
        self.template_file = os.path.join('reports', 'junit.xml')

    def build_report(self, filename, report_data):
        # Write the report
        with open(filename, 'w') as f:
            env = spack.tengine.make_environment()
            t = env.get_template(self.template_file)
            f.write(t.render(report_data))
