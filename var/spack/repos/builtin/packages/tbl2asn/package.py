# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import chmod

from spack import *


class Tbl2asn(Package):
    """Tbl2asn is a command-line program that automates the creation of
       sequence records for submission to GenBank."""

    homepage = "https://www.ncbi.nlm.nih.gov/genbank/tbl2asn2/"

    version('2020-03-01', sha256='b7edf378c971e6d7c48bf4d391d43a6d79f0e26dfa57156b4f87456af83e1fee')

    def url_for_version(self, ver):
        return "https://ftp.ncbi.nih.gov/toolbox/ncbi_tools/converters/by_program/tbl2asn/linux64.tbl2asn.gz"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('../linux64.tbl2asn', prefix.bin + '/tbl2asn')
        chmod(prefix.bin + '/tbl2asn', 0o775)
