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


class Kibana(Package):
    """Kibana lets you visualize your Elasticsearch data and navigate the
    Elastic Stack"""

    homepage = "https://www.elastic.co/products/kibana"
    url      = "https://artifacts.elastic.co/downloads/kibana/kibana-6.4.0-linux-x86_64.tar.gz"

    version('6.4.0', sha256='df2056105a08c206a1adf9caed09a152a53429a0f1efc1ba3ccd616092d78aee')

    depends_on('jdk', type='run')

    def install(self, spec, prefix):
        install_tree('.', join_path(prefix, '.'))
