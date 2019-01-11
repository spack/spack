# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
