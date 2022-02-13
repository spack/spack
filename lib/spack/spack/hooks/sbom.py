# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.sbom


def on_install_success(spec):
    """On the success of an install generate an sbom.
    """
    if not spack.sbom.generate_sbom:
        tty.debug("sbom generation not requested for %s" % spec)
        return

    tty.debug("Running hooks.sbom.on_install_success for %s" % spec)

    # Write sbom to the metadata directory
    spack.sbom.create_sbom(spec)
