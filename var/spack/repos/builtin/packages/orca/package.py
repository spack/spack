# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Orca(Package):
    """An ab initio, DFT and semiempirical SCF-MO package

       Note: Orca is licensed software. You will need to create an account
       on the Orca homepage and download Orca yourself. Spack will search
       your current directory for the download file. Alternatively, add this
       file to a mirror so that Spack can find it. For instructions on how to
       set up a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://cec.mpg.de"
    url      = "file://{0}/orca_4_0_1_2_linux_x86-64_openmpi202.tar.zst".format(os.getcwd())

    version('4.0.1.2', sha256='cea442aa99ec0d7ffde65014932196b62343f7a6191b4bfc438bfb38c03942f7',
            expand=False)

    depends_on('zstd', type='build')
    depends_on('openmpi@2.0.0:2.1.5', type='run')

    def url_for_version(self, version):
        out = "file://{0}/orca_{1}_linux_x86-64_openmpi202.tar.zst"
        return out.format(os.getcwd(), version.underscored)

    def install(self, spec, prefix):
        # we have to extract the archive ourself
        # fortunately it's just full of a bunch of binaries

        vername = os.path.basename(self.stage.archive_file).split('.')[0]

        zstd = which('zstd')
        zstd('-d', self.stage.archive_file, '-o', vername + '.tar')

        tar = which('tar')
        tar('-xvf', vername + '.tar')

        # there are READMEs in there but they don't hurt anyone
        mkdirp(prefix.bin)
        install_tree(vername, prefix.bin)
