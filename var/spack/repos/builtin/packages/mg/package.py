# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mg(Package):
    """Mg is intended to be a small, fast, and portable editor for people
    who can't (or don't want to) run emacs for one reason or another,
    or are not familiar with the vi editor. It is compatible with
    emacs because there shouldn't be any reason to learn more editor
    types than emacs or vi."""

    homepage = "https://github.com/ibara/mg"
    url      = "https://github.com/ibara/mg/archive/mg-6.6.tar.gz"

    version('6.8.1', sha256='a4af7afa77fed691096be8e2ff0507cc6bdd8efe7255916f714168d02790044c')
    version('6.8',   sha256='bc5f2445b755b362dd6651fe63e5433034044d9f3cd214fcad4cb739592e76bd')
    version('6.7',   sha256='02583d90df743e994fb1e411befbd23488fd1eaeb82c9db1fd4957d1a8f1abde')
    version('6.6', sha256='e8440353da1a52ec7d40fb88d4f145da49c320b5ba31daf895b0b0db5ccd0632')

    depends_on('ncurses')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        configure = Executable('./configure')
        args = [
            '--mandir={0}'.format(self.prefix.man),
            '--prefix={0}'.format(self.prefix),
        ]
        configure(*args)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make('install')
