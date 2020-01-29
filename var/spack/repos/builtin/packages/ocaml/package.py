# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ocaml(Package):
    """OCaml is an industrial strength programming language supporting
       functional, imperative and object-oriented styles"""

    homepage = "http://ocaml.org/"
    url      = "https://caml.inria.fr/pub/distrib/ocaml-4.06/ocaml-4.06.0.tar.gz"

    version('4.06.0', sha256='c17578e243c4b889fe53a104d8927eb8749c7be2e6b622db8b3c7b386723bf50')
    version('4.03.0', sha256='7fdf280cc6c0a2de4fc9891d0bf4633ea417046ece619f011fd44540fcfc8da2')

    depends_on('ncurses')

    def url_for_version(self, version):
        url = "http://caml.inria.fr/pub/distrib/ocaml-{0}/ocaml-{1}.tar.gz"
        return url.format(str(version)[:-2], version)

    def install(self, spec, prefix):
        configure('-prefix', '{0}'.format(prefix))

        make('world.opt')
        make('install', 'PREFIX={0}'.format(prefix))
