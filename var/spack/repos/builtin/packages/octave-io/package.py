# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OctaveIo(OctavePackage, SourceforgePackage):
    """The IO package is part of the Octave Forge project
    and provides input/output from/in external formats."""

    homepage = "https://octave.sourceforge.io/io/"
    sourceforge_mirror_path = "octave/io-2.6.3.tar.gz"

    version('2.6.3', sha256='6bc63c6498d79cada01a6c4446f793536e0bb416ddec2a5201dd8d741d459e10')

    extends('octave@3.6.0:')
