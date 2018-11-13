# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PopplerData(CMakePackage):
    """This package consists of encoding files for use with poppler. The
    encoding files are optional and poppler will automatically read them if
    they are present.  When installed, the encoding files enables poppler to
    correctly render CJK and Cyrrilic properly.  While poppler is licensed
    under the GPL, these encoding files have different license, and thus
    distributed separately."""

    homepage = "https://poppler.freedesktop.org/"
    url      = "https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz"

    version('0.4.9', '35cc7beba00aa174631466f06732be40')

    depends_on('cmake@2.6:', type='build')
