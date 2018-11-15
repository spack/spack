# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Mirdeep2(Package):
    """miRDeep2 is a completely overhauled tool which discovers microRNA genes
       by analyzing sequenced RNAs."""

    homepage = "https://www.mdc-berlin.de/8551903/en/"
    url      = "https://www.mdc-berlin.de/system/files/migrated_files/fiona/mirdeep2_0_0_8.zip"

    version('0.0.8', 'a707f7d7ad4a2975fb8b2e78c5bcf483')

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-pdf-api2', type=('build', 'run'))
    depends_on('bowtie')
    depends_on('viennarna')
    depends_on('squid')
    depends_on('randfold')

    def url_for_version(self, version):
        url = 'https://www.mdc-berlin.de/system/files/migrated_files/fiona/mirdeep2_{0}.zip'
        return url.format(version.underscored)

    def patch(self):
        with working_dir('src'):
            files = glob.iglob("*.pl")
            for file in files:
                change = FileFilter(file)
                change.filter('usr/bin/perl', 'usr/bin/env perl')
                change.filter('perl -W', 'perl')
                change.filter("../Rfam_for_miRDeep.fa",
                              "Rfam_for_miRDeep.fa")
                change.filter("../install_successful",
                              "install_successful")

    def install(self, spec, prefix):
        install_tree('src', prefix.bin)
        install('Rfam_for_miRDeep.fa', prefix.bin)
        # miRDeep looks for the install_sucessful file to check if you used
        # their automated install script which we'll just be kind of hacking
        # around
        touch(prefix.bin.install_successful)
