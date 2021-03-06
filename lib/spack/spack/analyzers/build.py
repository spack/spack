# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""A build analyzer is a class of analyzer that typically just uploads
already existing metadata files from a package spec install directory. They
are grouped with analyzers because they are conceptually the same - uploading
additional metadata about the build with the spack analyze command."""


import spack.monitor
from .base import AnalyzerBase

import os
import re


class ConfigArgsAnalyzer(AnalyzerBase):

    name = "config_args"
    outfile = "spack-analyzer-install-files.json"
    description = "config args loaded from spack-configure-args.txt"

    def run(self):
        """Given a directory name, return the json file to save the result to
        """
        config_file = os.path.join(self.meta_dir, "spack-configure-args.txt")
        return {self.name: spack.monitor.read_file(config_file)}


class EnvironmentVariablesAnalyzer(AnalyzerBase):

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
        lines = [x.strip() for x in lines if "export " not in x]
        result = {}

        # Dictionary comprehentions require 2.7
        for x in lines:
            result[x.split("=", 1)[0]] = x.split("=", 1)[1]
        return result


class InstallFilesAnalyzer(AnalyzerBase):

    name = "install_files"
    outfile = "spack-analyzer-install-files.json"
    description = "install file listing read from install_manifest.json"

    def run(self):
        """Given a directory name, return the json file to save the result to
        """
        manifest_file = os.path.join(self.meta_dir, "install_manifest.json")
        return {self.name: spack.monitor.read_json(manifest_file)}
