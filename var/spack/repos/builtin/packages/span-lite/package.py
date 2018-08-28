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
from shutil import copytree


class SpanLite(Package):
    """
    A single-file header-only version of a C++20-like span for C++98, C++11 and
    later
    """

    homepage = "https://github.com/martinmoene/span-lite"
    url      = "https://github.com/martinmoene/span-lite/archive/v0.3.0.tar.gz"

    version('0.3.0', sha256='e083f368167fe632f866956edaa2c7a7d57a33ffb0d8def9b9f1a9daa47834bb')
    version('0.2.0', sha256='6e3305fe868442410a00962a39fc59ed494cecc4f99fe2aff187e33932f06e46')
    version('0.1.0', sha256='0a84b9369f86beba326e2160b683fd0922f416ce136437751a9ed70afcc67a1c')

    def install(self, spec, prefix):
        copytree('include', prefix.include)
