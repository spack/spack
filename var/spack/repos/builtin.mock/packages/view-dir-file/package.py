# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


class ViewDirFile(Package):
    """Installs a <prefix>/bin/x where x is a file, in contrast to view-dir-dir"""
    homepage = "http://www.spack.org"
    url = "http://www.spack.org/downloads/aml-1.0.tar.gz"
    has_code = False

    version('0.1.0', sha256='cc89a8768693f1f11539378b21cdca9f0ce3fc5cb564f9b3e4154a051dcea69b')

    def install(self, spec, prefix):
        os.mkdir(os.path.join(prefix, 'bin'))
        with open(os.path.join(prefix, 'bin', 'x'), 'wb') as f:
            f.write(b'file')
