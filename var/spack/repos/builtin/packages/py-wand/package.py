# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWand(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://pypi.io/packages/source/W/Wand/Wand-0.5.6.tar.gz"

    version('0.5.6', sha256='d06b59f36454024ce952488956319eb542d5dc65f1e1b00fead71df94dbfcf88')

    depends_on('py-setuptools', type='build')
    depends_on('image-magick')
#
#    def install(self, spec, prefix):
#        # FIXME: Unknown build system
#        make()
#        make('install')
