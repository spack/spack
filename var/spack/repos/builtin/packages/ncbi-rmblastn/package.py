# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class NcbiRmblastn(AutotoolsPackage):
    """RMBlast search engine for NCBI"""

    homepage = "https://www.repeatmasker.org/RMBlast.html"
    url      = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.9.0/ncbi-blast-2.9.0+-src.tar.gz"

    version('2.11.0', sha256='d88e1858ae7ce553545a795a2120e657a799a6d334f2a07ef0330cc3e74e1954')
    version('2.9.0', sha256='a390cc2d7a09422759fc178db84de9def822cbe485916bbb2ec0d215dacdc257')

    # There is a corresponding gzipped patch file associated with each version.
    # According to the documentation, https://www.repeatmasker.org/RMBlast.html,
    # Download NCBI Blast+ and rmblast patch file:
    #   ncbi-blast-2.11.0+-src.tar.gz
    #   isb-2.11.0+-rmblast.patch.gz
    # The patch is downloaded and unzipped in the ncbi-rmblastn Spack package
    # directory to make it available for the patch directive.
    patch(
        'https://www.repeatmasker.org/isb-2.11.0+-rmblast.patch.gz',
        sha256='ce985abd3512834adb9ad3e4078fbf9608a33a2ee6538a1e94b641490c92f899',
        archive_sha256='0fc27781c2ea2f17645247e2f3775b5d18c56f0b62761a865347be745ea4f6be',
        when='@2.11.0'
    )
    patch(
        'https://www.repeatmasker.org/isb-2.9.0+-rmblast.patch.gz',
        sha256='ffa0845801aed11f4215b452532f3ff5b3dcb49ac8c14169568aaa585b9450ed',
        archive_sha256='e746ee480ade608052306fd21f015c8a323f27029f65399275216f9a4c882d59',
        when='@2.9.0'
    )
    depends_on('cpio', type='build')
    depends_on('boost')
    depends_on('lzo')

    configure_directory = 'c++'

    def url_for_version(self, version):
        url = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/{0}/ncbi-blast-{1}+-src.tar.gz"
        return url.format(version, version)

    def configure_args(self):
        args = [
            "--with-mt",
            "--without-debug",
            "--without-krb5",
            "--without-openssl",
            "--without-libuv",
            "--with-projects=scripts/projects/rmblastn/project.lst",
        ]
        return args
