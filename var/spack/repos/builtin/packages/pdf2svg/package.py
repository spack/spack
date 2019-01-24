# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pdf2svg(AutotoolsPackage):
    """A simple PDF to SVG converter using the Poppler and Cairo libraries."""

    homepage = "http://www.cityinthesky.co.uk/opensource/pdf2svg"
    url      = "https://github.com/dawbarton/pdf2svg/archive/v0.2.3.tar.gz"

    version('0.2.3', 'd398b3b1c1979f554596238a44f12123')
    version('0.2.2', 'f7e0d2213f9e1422cee9421e18f72553')

    depends_on('cairo', type='run')
    depends_on('poppler', type='run')
