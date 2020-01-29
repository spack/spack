# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('1.2.2', sha256='15e617179251041f4bf3910257bbb8398db987d863dd3cfc288bdd958de58f00')
    version('1.2.1', sha256='f210ece7a2def34b486c9ccfb75de8febd64487b2ea4a14a7fa0358f37eacc3b')

    depends_on('ocaml')  # Not a strict dependency, but recommended

    parallel = False

    def setup_build_environment(self, env):
        # Environment variable setting taken from
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/opam.rb
        env.set('OCAMLPARAM', 'safe-string=0,_')  # OCaml 4.06.0 compat

    def build(self, spec, prefix):
        make('lib-ext')
        make()
        make('man')
