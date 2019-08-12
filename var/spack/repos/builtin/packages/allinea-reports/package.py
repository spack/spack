# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AllineaReports(Package):
    """Allinea Performance Reports are the most effective way to characterize
    and understand the performance of HPC application runs. One single-page
    HTML report elegantly answers a range of vital questions for any HPC site
    """

    homepage = "http://www.allinea.com/products/allinea-performance-reports"

    version('6.0.4', '3f13b08a32682737bc05246fbb2fcc77')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['licences/Licence']
    license_vars = ['ALLINEA_LICENCE_FILE', 'ALLINEA_LICENSE_FILE']
    license_url = 'http://www.allinea.com/user-guide/reports/Installation.html'

    def url_for_version(self, version):
        # TODO: add support for other architectures/distributions
        url = "http://content.allinea.com/downloads/"
        return url + "allinea-reports-%s-Redhat-6.0-x86_64.tar" % version

    def install(self, spec, prefix):
        textinstall = Executable('./textinstall.sh')
        textinstall('--accept-licence', prefix)
