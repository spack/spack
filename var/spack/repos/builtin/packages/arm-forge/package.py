# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class ArmForge(Package):
    """Arm Forge is the complete toolsuite for software development - with
    everything needed to debug, profile, optimize, edit and build C, C++ and
    Fortran applications on Linux for high performance - from single threads
    through to complex parallel HPC codes with MPI, OpenMP, threads or CUDA."""

    homepage = "http://www.allinea.com/products/develop-allinea-forge"

    version('19.0.3', 'ca58987e2f4cc17c5d235cda0ac3771f')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['licences/Licence']
    license_vars = ['ALLINEA_LICENSE_DIR', 'ALLINEA_LICENCE_DIR',
                    'ALLINEA_LICENSE_FILE', 'ALLINEA_LICENCE_FILE']
    license_url = 'http://www.allinea.com/user-guide/forge/Installation.html'

    def url_for_version(self, version):
        # TODO: add support for other architectures/distributions
        url = "http://content.allinea.com/downloads/"
        return url + "arm-forge-%s-Redhat-7.0-x86_64.tar" % version

    def install(self, spec, prefix):
        os.system('./textinstall.sh --accept-licence ' + prefix)
