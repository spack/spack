# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Ampl(Package):
    """AMPL integrates a modeling language for describing optimization data, variables,
    objectives, and constraints; a command language for debugging models and analyzing
    results; and a scripting language for manipulating data and implementing
    optimization strategies."""

    homepage = "https://ampl.com/"
    manual_download = True

    # Use the version as you would expect the user to know it, not necessarily the
    # version as it appears in the file name.  To get the checksum, use sha256sum.
    version('20190529', sha256='c35a87d85055ae5fe41b68d4b4458f1fdbf80643890501eeaad35b134cb11a2d')

    # Licensing
    license_required = True
    license_files    = ['./ampl.lic']

    resourceList = [
        # [version, name, destination, placement, url ,sha256sum]
        ('20190529', 'amplapi', '.', 'amplapi', 'file://{0}/amplapi-linux64.2.0.0.zip'.format(os.getcwd()), 'a4abe111f142b862f11fcd8700f964b688d5d2291e9e055f6e7adbd92b0e243a'),
        ('20190529', 'amplide', '.', 'amplide', 'file://{0}/amplide-linux64.3.5.tgz'.format(os.getcwd()), 'c2163896df672b71901d2e46cd5cf1c1c4f0451e478ef32d0971705aaf86d6ac'),
        ('20190529', 'ampl_lic', '.', 'ampl_lic_temp', 'file://{0}/ampl_lic.linux-intel64.20190419.tgz'.format(os.getcwd()), '67fcf9f55549a6ee0b9c8ca683aedd875f8edfaa2cf3d9fe261e227d8b5e615d')
    ]

    for rsver, rsname, rsdest, rsplace, rsurl, rschecksum in resourceList:
        resource(when='@{0}'.format(rsver),
                 name=rsname,
                 url=rsurl,
                 sha256=rschecksum,
                 destination=rsdest,
                 placement=rsplace
                 )

    def url_for_version(self, version):
        return "file://{0}/ampl.linux-intel64.{1}.tgz".format(os.getcwd(), version)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
        env.prepend_path("PATH", join_path(self.prefix, 'amplide'))
        env.prepend_path("CPATH", join_path(self.prefix, 'amplapi', 'include'))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, 'amplapi', 'lib'))

    def install(self, spec, prefix):
        install_tree('.', prefix)

        for key in self.resources:
            for res in self.resources[key]:
                cd(res.fetcher.stage.source_path)
                install_tree('.', prefix)
