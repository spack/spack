# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-sina
#
# You can edit this file again by typing:
#
#     spack edit py-sina
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class PySina(PythonPackage):
    """Sina allows codes to store, query, and visualize their data through an easy-to-use Python API.
    Data that fits its recognized schema can be ingested into one or more supported backends.
    Sina's API is independent of backend and gives users the benefits of a database without requiring knowledge of one,
    allowing queries to be expressed in pure Python.
    Visualizations are also provided through Python

    Sina is intended especially for use with run metadata,
    allowing users to easily and efficiently find simulation runs that match some criteria.
    """

    homepage = "https://github.com/LLNL/Sina"
    git = "https://github.com/LLNL/Sina"

    # notify when the package is updated.
    maintainers = [
            'HaluskaR',
            'estebanpauli',
            'murray55',
            'doutriaux1',
            ]

    version('1.11.0', tag="v1.11.0")
    version('1.10.0', tag="v1.10.0")

    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest', type='test')
    depends_on('py-ujson', type=('build','run'))
    depends_on("py-sqlalchemy", type="run")
    depends_on("py-six", type="run")

    # Licensing
    license_required = False
    license_comment  = '#'
    license_files    = ['LICENSE']

    build_directory = 'python'
