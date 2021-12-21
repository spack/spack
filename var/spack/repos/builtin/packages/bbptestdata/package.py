# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Bbptestdata(CMakePackage):
    """Blue Brain Project scientific test data"""
    homepage = "https://bbpgitlab.epfl.ch/common/test/data"
    git = "git@bbpgitlab.epfl.ch:common/test/data.git"
    url = "git@bbpgitlab.epfl.ch:common/test/data.git"

    version('2.0.0', tag='2.0.0')
