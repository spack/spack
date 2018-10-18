# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#

from spack import *


class SentieonGenomics(Package):
    """Sentieon provides complete solutions for secondary DNA analysis.
    Our software improves upon BWA, GATK, Mutect, and Mutect2 based pipelines.
    The Sentieon tools are deployable on any CPU-based computing system. 
    Please set the path to the sentieon server with:
    export SENTIEON_LICENSE=[FQDN]:[PORT]"""

    homepage = "https://www.sentieon.com/"
    url      = "file://{0}/sentieon-genomics-201808.01.tar.gz".format(os.getcwd())

    version('201808.01', sha256='6d77bcd5a35539549b28eccae07b19a3b353d027720536e68f46dcf4b980d5f7')

    # Licensing.
    license_require = True
    license_vars = ['SENTIEON_LICENSE']

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('doc', prefix.doc)
        install_tree('etc', prefix.etc)
        install_tree('lib', prefix.lib)
        install_tree('libexec', prefix.libexec)
        install_tree('share', prefix.share)
