# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *

class Simrna(Package):
    """SimRNA is a tool for simulations of RNA conformational dynamics
    (folding, unfolding, multiple chain complex formation etc.), and its
    applications include RNA 3D structure prediction. SimRNA can be
    initiated with input files that include either the RNA sequence (or
    sequences) in a single line (similar to the Vienna format) or in the
    form of a structure written in PDB format. The PDB format should be
    simply the structure of the RNA with no heteroatoms or unusual names.
    In the current version readable residues are A, C, G and U only (i.e.
    no modified residues are supported as of yet).
    Useage:: MUST COPY prefix.data TO current_working_directory
            or the directory where you intend to use it. Else
            make a symbolic link to it.
    """

    homepage = "http://genesilico.pl/software/stand-alone/simrna"
    manual_download = True

    maintainers = ['dorton21']

    version('3.20', sha256='0886e3fee38d9d1450f93dffec785d23aa5ba6397f5ab4c15e7fb04a0175e140')

    phases = ['install']

    def url_for_version(self, version):
        return "file://{0}/SimRNA_64bitIntel_Linux.tgz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix)
