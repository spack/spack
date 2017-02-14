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
#

from spack import *


class RubyLibxml2(RubyPackage):
    """The Libxml-Ruby project provides Ruby language bindings for the GNOME
    Libxml2 XML toolkit."""

    homepage = "https://rubygems.org/gems/libxml-ruby"
    url      = "https://rubygems.org/downloads/libxml-ruby-2.9.0.gem"

    version('2.9.0', 'ff7a9da1b1450720d7d1ec9276db25ef', expand=False)

    depends_on('libxml2')

    def install(self, spec, prefix):
        gem('install', '--local', 'libxml-ruby-{0}.gem'.format(self.version))
