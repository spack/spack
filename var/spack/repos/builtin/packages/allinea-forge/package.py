# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AllineaForge(Package):
    """Allinea Forge is the complete toolsuite for software development - with
    everything needed to debug, profile, optimize, edit and build C, C++ and
    Fortran applications on Linux for high performance - from single threads
    through to complex parallel HPC codes with MPI, OpenMP, threads or CUDA."""

    homepage = "http://www.allinea.com/products/develop-allinea-forge"

    version('6.0', 'c85fec6d01680b5b46fea80111186244')
    version('7.0', '4c2f5b2ff83d494854df74e6df4be7be')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['licences/Licence']
    license_vars = ['ALLINEA_LICENCE_FILE', 'ALLINEA_LICENSE_FILE']
    license_url = 'http://www.allinea.com/user-guide/forge/Installation.html'

    def url_for_version(self, version):
        # TODO: add support for other architectures/distributions
        url = "http://content.allinea.com/downloads/"
        return url + "arm-forge-latest-Redhat-%s-x86_64.tar" % version

    def install(self, spec, prefix):
        bash = which("bash")
        bash('./textinstall.sh', '--accept-licence', prefix)
