# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class PyTensorflowHub(Package):
    """TensorFlow Hub is a library to foster the publication, discovery, and
    consumption of reusable parts of machine learning models."""

    homepage = "https://github.com/tensorflow/hub"
    url = "https://files.pythonhosted.org/packages/f4/1f/ca72fa5400954903aa6f3354142cd66374604384fb13429af9e41b12120d/tensorflow_hub-0.11.0-py2.py3-none-any.whl"

    version('0.11.0', sha256='19399a8abef10682b4f739a5aa78b43da3937df17f5d2afb0547945798787674', expand=False)

    extends('python')

    depends_on('python@3.6:',               type=('build', 'run'))
    depends_on('py-pip',                    type='build')
    depends_on('py-setuptools',             type='build')
    depends_on('py-tensorflow-estimator',   type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
