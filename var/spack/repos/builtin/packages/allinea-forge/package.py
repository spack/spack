##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import platform


def get_os_version_arch():
    # Allinea has a different download for each OS/distro/version/arch
    # See http://www.allinea.com/products/forge/download
    system = platform.system()
    machine = platform.machine()

    # Linux
    if system == 'Linux':

        distro = platform.linux_distribution()[0]
        version = Version(platform.linux_distribution()[1])

        # Red Hat Enterprise Linux
        if distro == 'Red Hat Enterprise Linux Server' or distro == 'CentOS':  # noqa
            my_distro = 'Redhat'

            # AMD/Intel
            if machine == 'x86_64':
                my_mach = 'x86_64'

                if version >= Version('7.0'):
                    my_ver = '7.0'
                elif version >= Version('6.0'):
                    my_ver = '6.0'
                elif version >= Version('5.7'):
                    my_ver = '5.7'
            # AMD/Intel
            elif machine == 'i686':
                my_mach = 'i686'

                if version >= Version('5.6'):
                    my_ver = '5.6'
            # POWER little-endian
            elif machine == 'ppc64le':
                my_mach = 'ppc64le'

                if version >= Version('7.2'):
                    my_ver = '7.2'
            # POWER big-endian
            elif machine == 'ppc64':
                my_mach = 'ppc64'

                if version >= Version('6.2'):
                    my_ver = '6.2'

        # SuSE Enterprise Linux Server
        elif distro == 'OpenSUSE':
            my_distro = 'Suse'

            # AMD/Intel
            if machine == 'x86_64':
                my_mach = 'x86_64'

                if version >= Version('12'):
                    my_ver = '12'
                elif version >= Version('11'):
                    my_ver = '11'

        # Ubuntu
        elif distro == 'Ubuntu':
            my_distro = 'Ubuntu'

            # AMD/Intel
            if machine == 'x86_64':
                my_mach = 'x86_64'

                if version >= Version('14.04'):
                    my_ver = '14.04'
                elif version >= Version('12.04'):
                    my_ver = '12.04'
            # ARM v8
            if machine == 'aarch64':
                my_mach = 'aarch64'

                if version >= Version('14.04'):
                    my_ver = '14.04'

        # BlueGene/Q
        elif distro == 'bgq':
            return 'bgq'

    # macOS
    elif system == 'Darwin':
        my_distro = 'MacOSX'
        version = Version(platform.mac_ver()[0])

        # AMD/Intel
        if machine == 'x86_64':
            my_mach = 'x86_64'

        if version >= Version('10.7.5'):
            my_ver = '10.7.5'

    # Windows
    elif system == 'Windows':
        my_distro = 'Windows'
        version = Version(platform.win32_ver()[0])

        # AMD/Intel
        if machine == 'x86_64':
            my_mach = 'x64'
        # AMD/Intel
        elif machine == 'i686':
            my_mach = 'x86'

        if version >= Version('6.1'):
            my_ver = '6.1'

    try:
        return '-'.join([my_distro, my_ver, my_mach])
    except:
        msg = "No download available for '{0}', '{1}', '{2}', '{3}'"
        raise InstallError(msg.format(system, distro, version, machine))


class AllineaForge(Package):
    """Allinea Forge is the complete toolsuite for software development - with
    everything needed to debug, profile, optimize, edit and build C, C++ and
    Fortran applications on Linux for high performance - from single threads
    through to complex parallel HPC codes with MPI, OpenMP, threads or CUDA."""

    homepage = "http://www.allinea.com/products/develop-allinea-forge"

    os_version_arch = get_os_version_arch()

    if os_version_arch == 'Redhat-7.0-x86_64':
        version('6.0.4', '5500d43f4a3a58ded95b2a2f4434c8a0')
    elif os_version_arch == 'Redhat-6.0-x86_64':
        version('6.0.4', 'df7f769975048477a36f208d0cd57d7e')
    elif os_version_arch == 'Ubuntu-14.04-x86_64':
        version('6.0.4', '5c8ad4bd41c1b60791c8156bf710095d')
    elif os_version_arch == 'MacOSX-10.7.5-x86_64':
        version('6.0.4', '3ee83901a2afbb255f09f8a2138dd46e')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['licences/Licence']
    license_vars = ['ALLINEA_LICENCE_FILE', 'ALLINEA_LICENSE_FILE']
    license_url = 'http://www.allinea.com/user-guide/forge/Installation.html'


    def url_for_version(self, version):
        os_version_arch = get_os_version_arch()
        system = platform.system()

        if system == 'Linux':
            ext = 'tar'
        elif system == 'Darwin':
            ext = 'dmg'
        elif system == 'Windows':
            ext = 'exe'

        base_url = "http://content.allinea.com/downloads"

        if system == 'Linux':
            return "{0}/allinea-forge-{1}-{2}.{3}".format(
                base_url, version, os_version_arch, ext)
        else:
            return "{0}/allinea-forge-client-{1}-{2}.{3}".format(
                base_url, version, os_version_arch, ext)

    def install(self, spec, prefix):
        textinstall = which('textinstall.sh')
        textinstall('--accept-licence', prefix)
