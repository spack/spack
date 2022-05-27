# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyLlnlSina(PythonPackage):
    """Sina allows codes to store, query, and visualize their data through an
    easy-to-use Python API. Data that fits its recognized schema can be ingested
    into one or more supported backends.
    Sina's API is independent of backend and gives users the benefits of a database
    without requiring knowledge of one, allowing queries to be expressed in pure
    Python.  Visualizations are also provided through Python.

    Sina is intended especially for use with run metadata,
    allowing users to easily and efficiently find simulation runs that match some
    criteria.
    """

    homepage = "https://github.com/LLNL/Sina"
    git = "https://github.com/LLNL/Sina.git"

    # notify when the package is updated.
    maintainers = [
        'HaluskaR',
        'estebanpauli',
        'murray55',
        'doutriaux1',
    ]
    version('1.11.0', tag="v1.11.0")
    version('1.10.0', tag="v1.10.0")

    # let's remove dependency on orjson
    patch('no_orjson.patch')
    depends_on('py-setuptools', type='build')
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-ujson', type=('build', 'run'))
    depends_on("py-sqlalchemy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))

    build_directory = 'python'
