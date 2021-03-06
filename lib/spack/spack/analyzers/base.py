# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""An analyzer base provides basic functions to run the analysis, save results,
and (optionally) interact with a Spack Monitor
"""

import spack.monitor
import llnl.util.tty as tty

import os


class AnalyzerBase:

    def __init__(self, spec, dirname=None):
        """An Analyzer is intended to run on one spec install, so the spec
        with its associated package is required on init. The child analyzer
        class should define an init function that super's the init here, and
        also check that the analyzer has all dependencies that it
        needs. If an analyzer subclass does not have dependencies, it does not
        need to define an init. An Analyzer should not be allowed to proceed
        if one or more dependencies are missing. The dirname, if defined,
        is an optional directory name to save to (instead of the default meta
        spack directory).
        """
        self.spec = spec
        self.dirname = dirname

        # An analyzer cannot be run if the spec isn't associated with a package
        if not hasattr(spec, "package") or not spec.package:
            tty.die("A spec can only be analyzed with an associated package.")
        self.meta_dir = os.path.dirname(spec.package.install_log_path)

        for required in ["name", "outfile", "description"]:
            if not hasattr(self, required):
                tty.die("Please add a %s attribute on the analyzer." % required)

    def run(self):
        """Given a spec with an installed package, run the analyzer on it.
        """
        raise NotImplementedError

    def get_outfile(self, dirname=None, outfile=None):
        """Given a directory name, return the json file to save the result to
        """
        dirname = dirname or self.dirname or self.meta_dir
        return os.path.join(dirname, 'analyze', outfile or self.outfile)

    def save_result(self, result, outdir=None, monitor=None):
        """Save a result to the associated spack monitor, if defined. This
        function is on the level of the analyzer because it might be
        the case that the result is large (appropriate for a single request)
        or that the data is organized differently (e.g., more than one
        request per result). If an analyzer subclass needs to over-write
        this function with a custom save, that is appropriate to do (see abi).
        """
        # Save the result to file in the .analyze folder
        outfile = self.get_outfile(outdir)

        # We maintain the structure in json with the analyzer as key so
        # that in the future, we could upload to a monitor server
        if result[self.name]:
            tty.info("Writing result to %s" % outfile)
            spack.monitor.write_json(result[self.name], outfile)

        if monitor:
            monitor.send_analyze_metadata(self.spec.package, result)
