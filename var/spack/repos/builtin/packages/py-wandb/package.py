# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWandb(PythonPackage):
    """A tool for visualizing and tracking your machine
       learning experiments."""

    homepage = "https://github.com/wandb/"
    pypi     = "wandb/wandb-0.10.1.tar.gz"

    version('0.10.1', sha256='d02427cda58a6618ba10a027a76d9e3f68ad923d35964b1b68785c49e5160009', deprecated=True)  # Listed as yanked

    depends_on('python@2.7:2,3.4:',         type=('build', 'run'))
    depends_on('py-setuptools',             type='build')
    depends_on('py-click@7:',               type=('build', 'run'))
    depends_on('py-gitpython@1:',           type=('build', 'run'))
    depends_on('py-python-dateutil@2.6.1:', type=('build', 'run'))
    depends_on('py-requests@2.0:2',         type=('build', 'run'))
    depends_on('py-promise@2.0:2',          type=('build', 'run'))
    depends_on('py-shortuuid@0.5:',         type=('build', 'run'))
    depends_on('py-six@1.13:',              type=('build', 'run'))
    depends_on('py-watchdog@0.8.3:',        type=('build', 'run'))
    depends_on('py-psutil@5.0:',            type=('build', 'run'))
    depends_on('py-sentry-sdk@0.4:',        type=('build', 'run'))
    depends_on('py-subprocess32@3.5.3:',    type=('build', 'run'))
    depends_on('py-dockerpy-creds@0.4:',    type=('build', 'run'))
    depends_on('py-configparser@3.8.1:',    type=('build', 'run'))
    depends_on('py-protobuf@3.12:',         type=('build', 'run'))
    depends_on('py-pyyaml',                 type=('build', 'run'))
    depends_on('py-typing',                 type=('build', 'run'), when='^python@:3.4')
    depends_on('py-enum34',                 type=('build', 'run'), when='^python@:3.3')
