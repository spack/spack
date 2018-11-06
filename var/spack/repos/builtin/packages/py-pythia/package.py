# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythia(PythonPackage):
    """Pythia refers to the Pyre framework and a collection of packages that
    interact with it, such as an interface to the ACIS solid modelling package.
    """

    homepage = "https://geodynamics.org/cig/software/pythia/"
    url      = "https://geodynamics.org/cig/software/github/pythia/v0.8.1.18/pythia-0.8.1.18.tar.gz"

    # import_modules = [
    #     'journal', 'opal', 'mpi', 'rigid', 'pulse', 'pyre', 'elc', 'blade',
    #     'acis', 'cig', 'journal.components', 'journal.colors',
    #     'journal.diagnostics', 'journal.services', 'journal.devices',
    #     'opal.content', 'opal.weaver', 'opal.components', 'opal.inventory',
    #     'opal.applications', 'mpi.scripts', 'pyre.idd', 'pyre.ipa',
    #     'pyre.util', 'pyre.filesystem', 'pyre.xml', 'pyre.units',
    #     'pyre.handbook', 'pyre.weaver', 'pyre.components', 'pyre.odb',
    #     'pyre.hooks', 'pyre.inventory', 'pyre.launchers', 'pyre.simulations',
    #     'pyre.scripts', 'pyre.applications', 'pyre.db', 'pyre.templates',
    #     'pyre.ipc', 'pyre.geometry', 'pyre.parsing', 'pyre.services',
    #     'pyre.schedulers', 'pyre.handbook.constants', 'pyre.handbook.elements',
    #     'pyre.weaver.mills', 'pyre.weaver.components', 'pyre.odb.common',
    #     'pyre.odb.dbm', 'pyre.odb.fs', 'pyre.inventory.pcs',
    #     'pyre.inventory.cfg', 'pyre.inventory.odb',
    #     'pyre.inventory.properties', 'pyre.inventory.validators',
    #     'pyre.inventory.pml', 'pyre.inventory.pml.parser',
    #     'pyre.geometry.operations', 'pyre.geometry.solids',
    #     'pyre.geometry.pml', 'pyre.geometry.pml.parser',
    #     'pyre.parsing.locators', 'blade.components', 'blade.pml',
    #     'blade.pml.parser', 'cig.geodyn', 'cig.cs', 'cig.short', 'cig.long',
    #     'cig.seismo', 'cig.mc', 'cig.magma'
    # ]

    version('0.8.1.18', sha256='f6025e6d70046dc71e375eded3d731506f8dd79e2e53b7e1436754439dcdef1e')

    depends_on('python@:2', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
