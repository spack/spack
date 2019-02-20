# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAspyYaml(PythonPackage):
    """Some extensions to pyyaml"""

    homepage = "https://github.com/asottile/aspy.yaml"
    url      = "https://files.pythonhosted.org/packages/23/53/e80eea1877989d7ea6cd055be5a0addd4b60223a9340c7b82017d1401f0a/aspy.yaml-1.1.2.tar.gz"

    version('1.1.2', sha256='5eaaacd0886e8b581f0e4ff383fb6504720bb2b3c7be17307724246261a41adf')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml', type=('build', 'run'))
