# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pam(AutotoolsPackage):
    """Linux Pluggable Authentication Modules"""

    homepage = "http://linux-pam.org/"
    url      = "http://linux-pam.org/library/Linux-PAM-1.3.0.tar.bz2"

    version('1.3.0', 'da4b2289b7cfb19583d54e9eaaef1c3a')
    version('1.2.1', '9dc53067556d2dd567808fd509519dd6')
    version('1.2.0', 'ee4a480d77b341c99e8b1375f8f180c0')

    def configure_args(self):
        prefix = self.spec.prefix
        return [
            '--includedir={0}/include/security'.format(prefix)]
