# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDiscover(PythonPackage):
    """Test discovery for unittest."""

    homepage = "https://pypi.python.org/pypi/discover"
    url      = "https://pypi.io/packages/source/d/discover/discover-0.4.0.tar.gz"

    version('0.4.0', '30bb643af4f5ea47fff572b5c346207d')
