# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGenshi(PythonPackage):
    """Python toolkit for generation of output for the web"""
    homepage = "https://genshi.edgewall.org/"
    url      = "http://ftp.edgewall.com/pub/genshi/Genshi-0.7.tar.gz"

    version('0.7', '54e64dd69da3ec961f86e686e0848a82')
    version('0.6.1', '372c368c8931110b0a521fa6091742d7')
    version('0.6', '604e8b23b4697655d36a69c2d8ef7187')

    depends_on("py-setuptools", type='build')
