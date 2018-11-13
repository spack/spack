# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAffine(PythonPackage):
    """Matrices describing affine transformation of the plane."""

    homepage = "https://github.com/sgillies/affine"
    url      = "https://github.com/sgillies/affine/archive/2.1.0.zip"

    depends_on('py-setuptools', type='build')

    version('2.1.0', '99cf61c3ef484f93da9dc062dfbce4b5')
