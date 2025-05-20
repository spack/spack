# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

from ..old_style_autotools.package import OldStyleAutotools


class OldStyleDerived(OldStyleAutotools):
    """Package used to verify that old-style packages work correctly when executing the
    installation procedure.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def configure_args(self):
        return ["--with-bar"] + super().configure_args()
