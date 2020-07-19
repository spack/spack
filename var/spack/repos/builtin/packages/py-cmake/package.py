# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCmake(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    url      = "https://files.pythonhosted.org/packages/bf/b6/bc83a846ac9ffbcb7f9490af135c42002e12f3adc8253c9e55c07de49cf3/cmake-3.18.0.tar.gz"

    version('3.18.0', sha256='52b98c5ee70b5fa30a8623e96482227e065292f78794eb085fdf0fecb204b79b')

    depends_on('cmake')
    depends_on('py-scikit-build')
