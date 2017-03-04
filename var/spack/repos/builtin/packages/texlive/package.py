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


class Texlive(Package):
    """TeX Live is a free software distribution for the TeX typesetting
       system"""

    homepage = "http://www.tug.org/texlive"

    # Pull from specific site because the texlive mirrors do not all
    # update in synchrony.
    #
    # BEWARE: TexLive updates their installs frequently (probably why
    # they call it *Live*...).  There is no good way to provide a 
    # repeatable install of the package.  We try to keep up with the 
    # digest values, but don't be surprised if this package is
    # briefly unbuildable.
    #
    version('live', 'ad230fa814d122084c13d75c0b135fda',
            url="http://ctan.math.utah.edu/ctan/tex-archive/systems/texlive/tlnet/install-tl-unx.tar.gz")

    # There does not seem to be a complete list of schemes.
    # Examples include:
    #   full scheme (everything)
    #   medium scheme (small + more packages and languages)
    #   small scheme (basic + xetex, metapost, a few languages)
    #   basic scheme (plain and latex)
    #   minimal scheme (plain only)
    # See:
    # https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-25025r6
    variant('scheme',  default="small",
            description='Package subset to install (e.g. full, small, basic)')

    depends_on('perl', type='build')

    def install(self, spec, prefix):
        # Using texlive's mirror system leads to mysterious problems,
        # in lieu of being able to specify a repository as a variant, hardwire
        # a particular (slow, but central) one for now.
        _repository='http://ctan.math.washington.edu/tex-archive/systems/texlive/tlnet/'
        env = os.environ
        env['TEXLIVE_INSTALL_PREFIX'] = prefix
        perl = which('perl')
        scheme = spec.variants['scheme'].value
        perl('./install-tl', '-scheme', scheme,
             '-repository', _repository,
             '-portable', '-profile', '/dev/null')
