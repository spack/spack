# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This package contains code for creating analyzers to extract Application
Binary Interface (ABI) information, along with simple analyses that just load
existing metadata.
"""

from __future__ import absolute_import

import llnl.util.tty as tty
from .abi import LibabigailAnalyzer
from .build import (
    InstallFilesAnalyzer,
    EnvironmentVariablesAnalyzer,
    ConfigArgsAnalyzer
)

import os

__all__ = [
    'LibabigailAnalyzer',
    'InstallFilesAnalyzer',
    'EnvironmentVariablesAnalyzer',
    'ConfigArgsAnalyzer'
]

# "all" cannot be an analyzer type
analyzer_types = {

    # Build analyzers are generally just uploading metadata that exists
    'install_files': InstallFilesAnalyzer,
    'environment_variables': EnvironmentVariablesAnalyzer,
    'config_args': ConfigArgsAnalyzer,

    # Abi Analyzers need to generate features for objects
    'abigail': LibabigailAnalyzer,
}


def list_all():
    """A helper function to list all analyzers and their descriptions
    """
    for name, analyzer in analyzer_types.items():
        tty.info("%-35s: %-35s" % (name, analyzer.description))


def create_package_analyze_dir(spec):
    """Given a spec, create the analyze folder in it's metadata folder. The
    spec requires an associated package.
    """
    # An analyzer cannot be run if the spec isn't associated with a package
    if not hasattr(spec, "package") or not spec.package:
        tty.die("A spec can only be analyzed with an associated package.")

    meta_dir = os.path.dirname(spec.package.install_log_path)
    analyze_dir = os.path.join(meta_dir, "analyze")
    if not os.path.exists(analyze_dir):
        tty.debug("Creating directory for analyze %s" % analyze_dir)
        os.mkdir(analyze_dir)


def get_analyzer(name):
    """Courtesy function to retrieve an analyzer, and exit on error if it
    does not exist.
    """
    if name in analyzer_types:
        return analyzer_types[name]
    tty.die("Analyzer %s does not exist" % name)
