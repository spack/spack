# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NoUrlOrVersion(Package):
    """Mock package that has no url and no version."""

    homepage = "https://example.com/"
