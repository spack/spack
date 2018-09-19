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
from glob import glob


class Bib2xhtml(Package):
    """bib2xhtml is a program that converts BibTeX files into HTML."""
    homepage = "http://www.spinellis.gr/sw/textproc/bib2xhtml/"
    url = 'http://www.spinellis.gr/sw/textproc/bib2xhtml/bib2xhtml-v3.0-15-gf506.tar.gz'

    version('3.0-15-gf506', 'a26ba02fe0053bbbf2277bdf0acf8645')

    def install(self, spec, prefix):
        # Add the bst include files to the install directory
        bst_include = join_path(prefix.share, 'bib2xhtml')
        mkdirp(bst_include)
        for bstfile in glob('html-*bst'):
            install(bstfile, bst_include)

        # Install the script and point it at the user's favorite perl
        # and the bst include directory.
        mkdirp(prefix.bin)
        install('bib2xhtml', prefix.bin)
        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env BSTINPUTS=%s perl' % bst_include,
                    join_path(prefix.bin, 'bib2xhtml'))
