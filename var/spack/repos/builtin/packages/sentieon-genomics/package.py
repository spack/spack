# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
from spack import *


class SentieonGenomics(Package):
    """Sentieon provides complete solutions for secondary DNA analysis.
    Our software improves upon BWA, GATK, Mutect, and Mutect2 based pipelines.
    The Sentieon tools are deployable on any CPU-based computing system.
    Please set the path to the sentieon license server with:

    Please append the following to your license.dat file located in the
    $SPACK_ROOT/etc/spack/licenses/SentieonGenomics/license.dat

    SERVER [FQDN]:[PORT]
    USE_SERVER

    Alternately you may run the below command with your license server
    details.

    export SENTIEON_LICENSE=[FQDN]:[PORT]

    Note: A manual download is required.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.sentieon.com/"
    url      = "file://{0}/sentieon-genomics-201808.01.tar.gz".format(os.getcwd())

    version('201808.01', sha256='6d77bcd5a35539549b28eccae07b19a3b353d027720536e68f46dcf4b980d5f7')

    # Licensing.
    license_require = True
    license_files   = ['licenses/license.dat']
    license_vars    = ['SENTIEON_LICENSE']
    license_url     = 'https://support.sentieon.com/manual/_downloads/Sentieon.pdf'

    def configure(self, spec, prefix):
        config = {
            'destinationFolder':   prefix,
            'licensePath':         self.global_license_file
        }

    def install(self, spec, prefix):
        self.configure(spec, prefix)
        install_tree('bin', prefix.bin)
        install_tree('doc', prefix.doc)
        install_tree('etc', prefix.etc)
        install_tree('lib', prefix.lib)
        install_tree('libexec', prefix.libexec)
        install_tree('share', prefix.share)
