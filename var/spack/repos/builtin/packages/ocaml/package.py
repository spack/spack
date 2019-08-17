# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ocaml(Package):
    """OCaml is an industrial strength programming language supporting
       functional, imperative and object-oriented styles"""

    homepage = "http://ocaml.org/"
    url      = "http://caml.inria.fr/pub/distrib/ocaml-4.03/ocaml-4.03.0.tar.gz"

    version('4.06.0', '66e5439eb63dbb8b8224cba5d1b20947')
    version('4.03.0', '43812739ea1b4641cf480f57f977c149')

    depends_on('ncurses')

    def url_for_version(self, version):
        url = "http://caml.inria.fr/pub/distrib/ocaml-{0}/ocaml-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def install(self, spec, prefix):
        configure('-prefix', '{0}'.format(prefix))

        make('world.opt')
        make('install', 'PREFIX={0}'.format(prefix))
