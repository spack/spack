# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
from spack import *


class Baurmc(AutotoolsPackage):
    """Baur's Monte Carlo package for simulating W+ gamma production at hadron
    colliders provides full electroweak calculation upto O(alpha) and contains
    higher order QCD corrections as well."""

    homepage = "https://twiki.cern.ch/twiki/bin/view/Sandbox/BaurMCInteface"
    url      = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/baurmc-1.0-src.tgz"

    tags = ['hep']

    version('1.0', sha256='de5027ed2e66028bed890760bee9d869e1e330ac7f7112ee5cb25868cea5c35b')

    def do_stage(self, mirror_only=False):
        # the tarball extracts to an intermediate directory -
        # move everything to the proper source dir
        super(Baurmc, self).do_stage(mirror_only)
        dn = os.listdir(self.stage.source_path)[0]
        for fn in os.listdir(join_path(self.stage.source_path, dn)):
            shutil.move(join_path(self.stage.source_path, dn, fn),
                        join_path(self.stage.source_path, fn))
        shutil.rmtree(join_path(self.stage.source_path, dn))

    def patch(self):
        filter_file('FC=g77',
                    'FC=gfortran',
                    'configure',
                    string=True)

    def configure_args(self):
        options = ['--userfflags=-fno-automatic',
                   '--enable-shared',
                   ]
        return options

    def install(self, a, b):
        install_tree('lib', self.prefix.lib)
