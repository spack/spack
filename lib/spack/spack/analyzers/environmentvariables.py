# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""An environment analyzer will read and parse the environment variables
file in the installed package directory, generating a json file that has
an index of key, value pairs for environment variables."""


import spack.monitor
from .analyzerbase import Analyzerbase

import os
import re


class Environmentvariables(Analyzerbase):

    name = "environment_variables"
    outfile = "spack-analyzer-environment-variables.json"
    description = "environment variables parsed from spack-build-env.txt"

    def run(self):
        """Given a directory name, return the json file to save the result to
        """
        env_file = os.path.join(self.meta_dir, "spack-build-env.txt")
        return {self.name: self._read_environment_file(env_file)}

    def _read_environment_file(self, filename):
        """Given an environment file, we want to read it, split by semicolons
        and new lines, and then parse down to the subset of SPACK_* variables.
        We assume that all spack prefix variables are not secrets, and unlike
        the install_manifest.json, we don't (at least to start) parse the values
        to remove path prefixes specific to user systems.
        """
        if not os.path.exists(filename):
            return
        content = spack.monitor.read_file(filename)

        # Filter down to lines, not export statements. I'm only using multiple
        # lines because of the length limit.
        lines = re.split("(;|\n)", content)
        lines = [x for x in lines if x not in ['', '\n', ';'] and "SPACK_" in x]
        lines = [x.strip() for x in lines if "export " not in x]

        # Dictionary comprehentions require 2.7
        return dict(x.partition("=")[::2] for x in lines)
