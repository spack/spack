# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform

def getDistroName():
    distro = platform.linux_distribution()
    name = distro[0]
    if name.startswith('Red'):
        name = 'Redhat'
    elif name.startswith('Ubuntu'):
        name = 'Ubuntu'
    return name

class AllineaForge(Package):
    """Allinea Forge is the complete toolsuite for software development - with
    everything needed to debug, profile, optimize, edit and build C, C++ and
    Fortran applications on Linux for high performance - from single threads
    through to complex parallel HPC codes with MPI, OpenMP, threads or CUDA."""

    homepage = "http://www.allinea.com/products/develop-allinea-forge"

    # Default versions: Redhat
    version('latest', '585490ed224c71896f89b78b4d1629a6', preferred=True)
    version('19.0.1', 'ab1158398e72de75ea32d62abaf17649')
    version('19.0', '4c2f5b2ff83d494854df74e6df4be7be')
    version('18.3', '0188fb8a0b35b49c342927ce0ba9d552')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['licences/Licence']
    license_vars = ['ALLINEA_LICENCE_FILE', 'ALLINEA_LICENSE_FILE']
    license_url = 'http://www.allinea.com/user-guide/forge/Installation.html'

    conflicts('platform=darwin')

    def url_for_version(self, version):
        url = "http://content.allinea.com/downloads/arm-forge-{0}-{1}-x86_64.tar"
        # TODO: add support for other architectures/distributions/distroversions
        distro = getDistroName()

        if distro == 'Ubuntu':
            checksums = {
                Version('latest'): 'd8396b046e9b7f4241d69466f6155790',
                Version('19.0.1'): '67f6f05352ee9991acb844e032282b09',
                Version('19.0'): 'bf032f88c9294d839790886f83e9ce20',
                Version('18.3'): 'a1a3b1c6409881e1051bb5de66eaa9f2'
            }
            self.versions[version] = {'checksum': checksums[version]}
            return url.format(version, 'Ubuntu-16.04')
        return url.format(version, 'Redhat-7.0')

    def install(self, spec, prefix):
        bash = which("bash")
        bash('./textinstall.sh', '--accept-licence', prefix)
