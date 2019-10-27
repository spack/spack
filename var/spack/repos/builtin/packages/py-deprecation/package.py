# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeprecation(PythonPackage):
    """The deprecation library provides a deprecated decorator and a
    fail_if_not_removed decorator for your tests. """

    homepage = "http://deprecation.readthedocs.io/"
    url      = "https://pypi.io/packages/source/d/deprecation/deprecation-2.0.7.tar.gz"
    git      = "https://github.com/briancurtin/deprecation.git"

    version('2.0.7', tag='2.0.7')
    version('2.0.6', tag='2.0.6')
    version('2.0.5', tag='2.0.5')
    version('2.0.4', tag='2.0.4')
    version('2.0.3', tag='2.0.3')
    version('2.0.2', tag='2.0.2')
    version('2.0.1', tag='2.0.1')
    version('2.0.0', tag='2.0')
    version('1.2.0', tag='1.2')
    version('1.1.0', tag='1.1')
    version('1.0.1', tag='1.0.1')

    depends_on('py-setuptools', type='build')
