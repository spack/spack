# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTensorboardPluginWit(Package):
    """The What-If Tool makes it easy to efficiently and
       intuitively explore up to two models' performance
       on a dataset. Investigate model performances for
       a range of features in your dataset, optimization
       strategies and even manipulations to individual
       datapoint values. All this and more, in a visual way
       that requires minimal code."""

    homepage = "https://pypi.org/project/tensorboard-plugin-wit/"
    url      = "https://pypi.io/packages/py3/t/tensorboard_plugin_wit/tensorboard_plugin_wit-1.8.0-py3-none-any.whl"

    maintainers = ['aweits']

    version('1.8.0',
            sha256='2a80d1c551d741e99b2f197bb915d8a133e24adb8da1732b840041860f91183a',
            expand=False)
    version('1.7.0',
            sha256='ee775f04821185c90d9a0e9c56970ee43d7c41403beb6629385b39517129685b',
            expand=False)

    extends('python')

    depends_on('python@3.2:', type=('build', 'run'))
    depends_on('py-pip', type='build')

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', '--prefix={0}'.format(prefix), self.stage.archive_file)
