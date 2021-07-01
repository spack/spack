# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Ampl(Package):
    """AMPL integrates a modeling language for describing optimization data, variables,
    objectives, and constraints; a command language for debugging models and analyzing
    results; and a scripting language for manipulating data and implementing
    optimization strategies."""

    homepage = "https://ampl.com/"
    manual_download = True

    # Use the version as you would expect the user to know it, not necessarily the
    # version as it appears in the file name.  To get the checksum, use sha256sum.
    version('20210226', sha256='d9ffaed591c0491e311a44c2b246d9d81785f6c0b2747a7e32a783e522e18450')
    version('20190529', sha256='c35a87d85055ae5fe41b68d4b4458f1fdbf80643890501eeaad35b134cb11a2d')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files    = ['ampl.lic']
    license_url = 'https://ampl.com/resources/floating-licenses/installation/'

    resourceList = [
        # [version, name, destination, placement, url ,sha256sum]
        ('20210226', 'amplapi', '', 'amplapi', 'file://{0}/amplapi-linux64.2.0.0.zip'.format(os.getcwd()), 'a4abe111f142b862f11fcd8700f964b688d5d2291e9e055f6e7adbd92b0e243a'),
        ('20210226', 'amplide', '', 'amplide', 'file://{0}/amplide-linux64.3.5.tgz'.format(os.getcwd()), 'c2163896df672b71901d2e46cd5cf1c1c4f0451e478ef32d0971705aaf86d6ac'),
        ('20190529', 'amplapi', '', 'amplapi', 'file://{0}/amplapi-linux64.2.0.0.zip'.format(os.getcwd()), 'a4abe111f142b862f11fcd8700f964b688d5d2291e9e055f6e7adbd92b0e243a'),
        ('20190529', 'amplide', '', 'amplide', 'file://{0}/amplide-linux64.3.5.tgz'.format(os.getcwd()), 'c2163896df672b71901d2e46cd5cf1c1c4f0451e478ef32d0971705aaf86d6ac'),
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

    def install(self, spec, prefix):
        install_tree('.', prefix)
        install_tree('amplapi', prefix)
        install_tree('amplide', prefix)
