# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import tarfile
import fnmatch
import os


class Minigan(PythonPackage):
    """miniGAN is a generative adversarial network code developed as part of the
    Exascale Computing Project's (ECP) ExaLearn project at
    Sandia National Laboratories."""

    homepage = "https://github.com/SandiaMLMiniApps/miniGAN"
    url      = "https://github.com/SandiaMLMiniApps/miniGAN/archive/1.0.0.tar.gz"

    version('1.0.0', sha256='ef6d5def9c7040af520acc64b7a8b6c8ec4b7901721b11b0cb25a583ea0c8ae3')

    depends_on('python', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-torch')
    depends_on('py-numpy')
    depends_on('py-horovod@master')
    depends_on('py-torchvision')
    depends_on('py-matplotlib@3.0.0')

    phases = ['install']

    def install(self, spec, prefix):
        for file in os.listdir(prefix):
            if fnmatch.fnmatch(file, '*.tar.gz'):
                tf = tarfile.extract(filename)
                tf.extractall()
