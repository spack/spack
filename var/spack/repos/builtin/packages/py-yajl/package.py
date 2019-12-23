# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from shutil import rmtree
from os import symlink


class PyYajl(PythonPackage):
    """Python bindings for the Yajl JSON encoder/decoder library."""

    homepage = "https://github.com/rtyler/py-yajl"
    url      = "https://github.com/rtyler/py-yajl/archive/v0.3.5.tar.gz"

    version('0.3.5', sha256='59c7f951086a8b35ac5f12b55030b4d23cb4eb5304520390f5b3a345a9c18cef')

    resource(
        name='yajl',
        git='https://github.com/lloyd/yajl.git',
        commit='d1e770838efaa76811f1cd8930d19d13b14fbc2b',
        destination='yajlsrc',
    )

    depends_on('py-setuptools', type='build')

    # py-yajl source comes with an empty 'yajl' directory which interferes with
    # resource expansion -- manually remove it and replace with the resource
    @run_before('build')
    def prep_yajl(self):
        rmtree('yajl')
        symlink('yajlsrc/yajl', 'yajl')
