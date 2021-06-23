# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBeniget(PythonPackage):
    """Extract semantic information about static Python code."""

    homepage = "https://github.com/serge-sans-paille/beniget/"
    pypi     = "beniget/beniget-0.3.0.tar.gz"

    version('0.3.0', sha256='062c893be9cdf87c3144fb15041cce4d81c67107c1591952cd45fdce789a0ff1')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-gast@0.4.0:0.4.999', type=('build', 'run'))
