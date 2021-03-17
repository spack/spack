# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""A configargs analyzer is a class of analyzer that typically just uploads
already existing metadata about config args from a package spec install
directory."""


import spack.monitor
from .analyzerbase import Analyzerbase

import os


class Configargs(Analyzerbase):

    name = "config_args"
    outfile = "spack-analyzer-install-files.json"
    description = "config args loaded from spack-configure-args.txt"

    def run(self):
        """Given a directory name, return the json file to save the result to
        """
        config_file = os.path.join(self.meta_dir, "spack-configure-args.txt")
        return {self.name: spack.monitor.read_file(config_file)}
