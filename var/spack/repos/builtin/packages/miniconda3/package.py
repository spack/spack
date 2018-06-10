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
from six.moves.urllib.parse import urlparse
from os.path import split


class Miniconda3(Package):
    """The minimalist bootstrap toolset for conda and Python3."""

    homepage = "https://conda.io/miniconda.html"
    url      = "https://repo.continuum.io/miniconda/Miniconda3-4.3.11-Linux-x86_64.sh"

    version('4.5.4', 'a946ea1d0c4a642ddf0c3a26a18bb16d', expand=False)
    version('4.3.30', '0b80a152332a4ce5250f3c09589c7a81', expand=False)
    version('4.3.14', 'fc6fc37479e3e3fcf3f9ba52cae98991', expand=False)
    version('4.3.11', '1924c8d9ec0abf09005aa03425e9ab1a', expand=False)

    def install(self, spec, prefix):
        # peel the name of the script out of the url
        result = urlparse(self.url)
        dir, script = split(result.path)
        bash = which('bash')
        bash(script, '-b', '-f', '-p', self.prefix)
