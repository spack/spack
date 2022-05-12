# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SentieonGenomics(Package):
    """Sentieon provides complete solutions for secondary DNA analysis.
    Our software improves upon BWA, GATK, Mutect, and Mutect2 based pipelines.
    The Sentieon tools are deployable on any CPU-based computing system.

    Use of this software is subject to the EULA at:
    https://www.sentieon.com/EULA/eula-aws.html

    Please set the path to the sentieon license server with:

    export SENTIEON_LICENSE=[FQDN]:[PORT]
    """

    homepage = "https://www.sentieon.com/"
    # url is from the permalink documented in dockerfile at
    # https://github.com/Sentieon/sentieon-docker/blob/master/Dockerfile
    # See also: https://github.com/spack/spack/pull/30145/files#r853275635
    url      = "https://s3.amazonaws.com/sentieon-release/software/sentieon-genomics-201808.01.tar.gz"
    maintainers = ['snehring']

    version('202112.02', sha256='033943df7958550fd42b410d34ae91a8956a905fc90ca8baa93d2830f918872c')
    version('201808.07', sha256='fb66b18a7b99e44968eb2c3a6a5b761d6b1e70fba9f7dfc4e5db3a74ab3d3dd9')
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
