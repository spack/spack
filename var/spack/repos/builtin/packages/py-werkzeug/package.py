# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyWerkzeug(PythonPackage):
    """The Swiss Army knife of Python web development"""

    homepage = "http://werkzeug.pocoo.org"
    pypi = "Werkzeug/Werkzeug-0.16.0.tar.gz"

    version('2.0.2',   sha256='aa2bb6fc8dee8d6c504c0ac1e7f5f7dc5810a9903e793b6f715a9f015bdadb9a')
    version('0.16.0',  sha256='7280924747b5733b246fe23972186c6b348f9ae29724135a6dfc1e53cea433e7')
    version('0.15.6',  sha256='0a24d43be6a7dce81bae05292356176d6c46d63e42a0dd3f9504b210a9cfaa43')
    version('0.15.5',  sha256='a13b74dd3c45f758d4ebdb224be8f1ab8ef58b3c0ffc1783a8c7d9f4f50227e6')
    version('0.15.4',  sha256='a0b915f0815982fb2a09161cb8f31708052d0951c3ba433ccc5e1aa276507ca6')
    version('0.15.3',  sha256='cfd1281b1748288e59762c0e174d64d8bcb2b70e7c57bc4a1203c8825af24ac3')
    version('0.15.2',  sha256='0a73e8bb2ff2feecfc5d56e6f458f5b99290ef34f565ffb2665801ff7de6af7a')
    version('0.15.1',  sha256='ca5c2dcd367d6c0df87185b9082929d255358f5391923269335782b213d52655')
    version('0.15.0',  sha256='590abe38f8be026d78457fe3b5200895b3543e58ac3fc1dd792c6333ea11af64')
    version('0.11.15', sha256='455d7798ac263266dbd38d4841f7534dd35ca9c3da4a8df303f8488f38f3bcc0')
    version('0.11.11', sha256='e72c46bc14405cba7a26bd2ce28df734471bc9016bc8b4cb69466c2c14c2f7e5')

    depends_on('python@3.6:', when='@2:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-dataclasses', when='@2: ^python@:3.6', type=('build', 'run'))
