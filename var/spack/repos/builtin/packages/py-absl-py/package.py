# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class PyAbslPy(PythonPackage):
    """
    This repository is a collection of Python library code for building Python applications.
    The code is collected from Google's own Python code base, and has been extensively tested and used in production.
    """

    homepage = "https://pypi.org/project/absl-py/"
    url      = "https://cosmo-pypi.phys.ethz.ch/simple/absl-py/0.1.6/absl-py-0.1.6.tar.gz"

    version('0.1.6', 'b76269cbf04502b7d12efabcfa51a299')

    depends_on('py-six@1.10.0:', type='build')
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3.99')
    depends_on('py-setuptools', type='build')
