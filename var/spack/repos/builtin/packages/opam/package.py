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


class Opam(AutotoolsPackage):
    """OPAM: OCaml Package Manager

       OPAM is a source-based package manager for OCaml. It supports
       multiple simultaneous compiler installations, flexible package
       constraints, and a Git-friendly development workflow."""

    homepage = "https://opam.ocaml.org/"
    url      = "https://github.com/ocaml/opam/releases/download/1.2.2/opam-full-1.2.2.tar.gz"

    version('1.2.2', '7d348c2898795e9f325fb80eaaf5eae8')
    version('1.2.1', '04e8823a099ab631943952e4c2ab18fc')

    depends_on('ocaml')  # Not a strict dependency, but recommended

    parallel = False

    def setup_environment(self, spack_env, run_env):
        # Environment variable setting taken from
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/opam.rb
        spack_env.set('OCAMLPARAM', 'safe-string=0,_')  # OCaml 4.06.0 compat

    def build(self, spec, prefix):
        make('lib-ext')
        make()
        make('man')
