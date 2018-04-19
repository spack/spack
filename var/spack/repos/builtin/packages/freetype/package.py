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


class Freetype(AutotoolsPackage):
    """FreeType is a freely available software library to render fonts.
    It is written in C, designed to be small, efficient, highly customizable,
    and portable while capable of producing high-quality output (glyph images)
    of most vector and bitmap font formats."""

    homepage = "https://www.freetype.org/index.html"
    url      = "http://download.savannah.gnu.org/releases/freetype/freetype-2.7.1.tar.gz"

    version('2.7.1', '78701bee8d249578d83bb9a2f3aa3616')
    version('2.7',   '337139e5c7c5bd645fe130608e0fa8b5')
    version('2.5.3', 'cafe9f210e45360279c730d27bf071e9')

    depends_on('libpng')
    depends_on('bzip2')
    depends_on('pkgconfig', type='build')

    def configure_args(self):
        return ['--with-harfbuzz=no']

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path('CPATH', self.prefix.include.freetype2)
        run_env.prepend_path('CPATH', self.prefix.include.freetype2)
