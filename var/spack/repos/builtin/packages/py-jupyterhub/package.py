# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterhub(PythonPackage):
    """Multi-user server for Jupyter notebooks."""

    pypi = "jupyterhub/jupyterhub-1.0.0.tar.gz"

    version('1.3.0', sha256='05ff701209c340c792cd103606c448c52ace772ece858380905ddd1a2136ee8e')
    version('1.2.2', sha256='634e64ab9cf14e73cfc1d5838d595febdaf957607eb907b43f29af345c05b87e')
    version('1.2.1', sha256='4d24e064db10c1d070696c7a3dee55739a24db6990051aa296e708910d1b14b9')
    version('1.2.0', sha256='fa3c2530fcb3330a95e5263191b411d61ae2ea7d32744b342d9db245a455edea')
    version('1.1.0', sha256='852a70225a03abd631b36a207f3ffdf69326a0db4cef539825fde39ec1b713d7')
    version('1.0.0',    sha256='33541a515a041b9a518ca057c1c4ab4215a7450fdddc206401713ee8137fa67f')
    version('0.9.4',    sha256='7848bbb299536641a59eb1977ec3c7c95d931bace4a2803d7e9b28b9256714da')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-sqlalchemy@1.1:', type=('build', 'run'))
    depends_on('py-tornado@5.0:', type=('build', 'run'))
    depends_on('py-traitlets@4.3.2:', type=('build', 'run'))
    depends_on('py-alembic', type=('build', 'run'))
    depends_on('py-mako', type=('build', 'run'))
    depends_on('py-async-generator@1.8:', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-certipy@0.1.2:', when='@1.0.0:',  type=('build', 'run'))
    depends_on('py-entrypoints', when='@1.0.0:',  type=('build', 'run'))
    depends_on('py-oauthlib@3.0:', when='@1.0.0:', type=('build', 'run'))
    depends_on('py-python-oauth2@1.0:', when='@:9.4', type=('build', 'run'))
    depends_on('py-pamela', type=('build', 'run'))
    depends_on('py-notebook', type=('build', 'run'))
    depends_on('py-prometheus-client@0.0.21:', type=('build', 'run'))
