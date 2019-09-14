# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scantailor(CMakePackage):
    """Scan Tailor is an interactive post-processing tool for scanned pages. It
    performs operations such as page splitting, deskewing, adding/removing
    borders, and others. You give it raw scans, and you get pages ready to be
    printed or assembled into a PDF or DJVU file. Scanning, optical character
    recognition, and assembling multi-page documents are out of scope of this
    project."""

    homepage = "http://www.scantailor.org"
    _url_fmt = (
        "https://github.com/scantailor/scantailor/archive/RELEASE_{}.tar.gz"
    )
    url = "https://github.com/scantailor/scantailor/archive/RELEASE_0_9_12_1.tar.gz"

    version(
        "0_9_12_2",
        sha256="1f7b96bbe5179d46e332aea8d51ba50545fe7c510811e51588b6a4919e4feeab",
    )

    depends_on("qt@4.4:4.8")
    depends_on("libjpeg")
    depends_on("zlib")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("boost@1.35:")
    depends_on("libxrender")

    patch("boost_unit_test.patch")

    def url_for_version(self, version):
        return self._url_fmt.format(version.underscored)
