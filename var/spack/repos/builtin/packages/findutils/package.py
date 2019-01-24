# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Findutils(AutotoolsPackage):
    """The GNU Find Utilities are the basic directory searching
       utilities of the GNU operating system."""

    homepage = "https://www.gnu.org/software/findutils/"
    url      = "https://ftpmirror.gnu.org/findutils/findutils-4.6.0.tar.gz"

    version('4.6.0',  '9936aa8009438ce185bea2694a997fc1')
    version('4.4.2',  '351cc4adb07d54877fa15f75fb77d39f')
    version('4.4.1',  '5883f569dc021eee765f330bb7a3782d')
    version('4.4.0',  '49e769ac4382fae6f104f99d54d0a112')
    version('4.2.33', 'b7e35aa175778c84942b1fee4144988b')
    version('4.2.32', 'aaa6beeb41a6f04963dff58f24a55b96')
    version('4.2.31', 'a0e31a0f18a49709bf5a449867c8049a')
    version('4.2.30', 'c35ff6502e0b3514c99089cb5d333c25')
    version('4.2.29', '24e76434ca74ba3c2c6ad621eb64e1ff')
    version('4.2.28', 'f5fb3349354ee3d94fceb81dab5c71fd')
    version('4.2.27', 'f1e0ddf09f28f8102ff3b90f3b5bc920')
    version('4.2.26', '9ac4e62937b1fdc4eb643d1d4bf117d3')
    version('4.2.25', 'e92fef6714ffa9972f28a1a423066921')
    version('4.2.23', 'ecaff8b060e8d69c10eb2391a8032e26')
    version('4.2.20', '7c8e12165b221dd67a19c00d780437a4')
    version('4.2.18', '8aac2498435f3f1882678fb9ebda5c34')
    version('4.2.15', 'a881b15aa7170aea045bf35cc92d48e7')
    version('4.1.20', 'e90ce7222daadeb8616b8db461e17cbc')
    version('4.1',    '3ea8fe58ef5386da75f6c707713aa059')

    depends_on('autoconf', type='build', when='@4.6.0')
    depends_on('automake', type='build', when='@4.6.0')
    depends_on('libtool', type='build', when='@4.6.0')
    depends_on('m4', type='build', when='@4.6.0')
    depends_on('texinfo', type='build', when='@4.6.0')

    # findutils does not build with newer versions of glibc
    patch('https://src.fedoraproject.org/rpms/findutils/raw/97ba2d7a18d1f9ae761b6ff0b4f1c4d33d7a8efc/f/findutils-4.6.0-gnulib-fflush.patch', sha256='84b916c0bf8c51b7e7b28417692f0ad3e7030d1f3c248ba77c42ede5c1c5d11e', when='@4.6.0')
    patch('https://src.fedoraproject.org/rpms/findutils/raw/97ba2d7a18d1f9ae761b6ff0b4f1c4d33d7a8efc/f/findutils-4.6.0-gnulib-makedev.patch', sha256='bd9e4e5cc280f9753ae14956c4e4aa17fe7a210f55dd6c84aa60b12d106d47a2', when='@4.6.0')

    build_directory = 'spack-build'

    @property
    def force_autoreconf(self):
        # Run autoreconf due to build system patch (gnulib-makedev)
        return self.spec.satisfies('@4.6.0')

    @when('@4.6.0')
    def patch(self):
        # We have to patch out gettext support, otherwise autoreconf tries to
        # call autopoint, which depends on find, which is part of findutils.
        filter_file('^AM_GNU_GETTEXT.*',
                    '',
                    'configure.ac')

        filter_file(r'^SUBDIRS = (.*) po (.*)',
                    r'SUBDIRS = \1 \2',
                    'Makefile.am')
