# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack
import spack.binary_distribution
import spack.package
import spack.repo

import llnl.util.tty as tty

from .base import AnalyzerBase

import os


class LibabigailAnalyzer(AnalyzerBase):

    name = "libabigail"
    outfile = "spack-analyzer-libabigail.json"
    description = "Application Binary Interface (ABI) features for objects"
    saves_internally = True

    def __init__(self, spec, monitor=None, dirname=None):
        """init for an analyzer is where we want to ensure that we have all
        needed dependencies. For the abigail analyzer, this means Libabigail.
        Since the output for libabigail is one file per object, we communicate
        with the monitor multiple times.
        """
        super().__init__(spec, monitor, dirname)

        # This doesn't seem to work to import on the module level
        import spack.bootstrap
        tty.debug("Preparing to use Libabigail, will install if missing.")

        with spack.bootstrap.ensure_bootstrap_configuration():

            # libabigail won't install lib/bin/share without docs
            spec = spack.spec.Spec("libabigail+docs")
            spec.concretize()
            self.abidw = spack.bootstrap.get_executable(
                "abidw", spec=spec, install=True)

    def run(self):
        """Given a directory name, return the json file to save the result to
        """
        manifest = spack.binary_distribution.get_buildfile_manifest(self.spec)

        # Generate an output file for each binary or object
        for obj in manifest.get("binary_to_relocate_fullpath", []):

            outfile = "spack-analyzer-libabigail-%s.xml" % os.path.basename(obj)
            outfile = self.get_outfile(self.dirname, outfile=outfile)
            self.abidw(obj, "--out-file", outfile)
            # TODO need to send to monitor here

        # not written yet
        return {self.name: {}}
