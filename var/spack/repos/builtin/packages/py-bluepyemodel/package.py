# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBluepyemodel(PythonPackage):
    """Python library to optimize and evaluate electrical models."""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/cells/BluePyEModel"
    git      = "ssh://bbpcode.epfl.ch/cells/BluePyEModel"

    version('0.0.5', tag='BluePyEModel-v0.0.5')

    depends_on('py-setuptools', type='build')

    depends_on('neuron', type='run')
    depends_on('py-bluepy@2.3.0:', type='run')
    depends_on('py-bluepyefe@BPE2', type='run')
    depends_on('py-bluepyopt', type='run')
    depends_on('py-bluepyparallel@0.0.3:', type='run')
    depends_on('py-click@7.0:', type='run')
    depends_on('py-efel@3.0.80:', type='run')
    depends_on('py-fasteners@0.14:', type='run')
    depends_on('py-gitpython', type='run')
    depends_on('py-h5py@2.9:', type='run')
    depends_on('py-ipyparallel@6.3:', type='run')
    depends_on('py-matplotlib@2.2:', type='run')
    depends_on('py-morph-tool@2.5.1:', type='run')
    depends_on('py-numpy@1.15.0:', type='run')
    depends_on('py-pandas@0.24:', type='run')
    depends_on('py-psycopg2', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-tqdm@4.28.1:', type='run')
