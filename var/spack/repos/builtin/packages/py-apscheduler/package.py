# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyApscheduler(PythonPackage):
    """In-process task scheduler with Cron-like capabilities."""

    homepage = "https://github.com/agronholm/apscheduler"
    url      = "https://pypi.io/packages/source/A/APScheduler/APScheduler-3.3.1.tar.gz"

    version('3.3.1', '6342b3b78b41920a8aa54fd3cd4a299d')
    version('2.1.0', 'b837d23822fc46651862dd2186ec361a')

    depends_on('py-setuptools@0.7:', type='build')

    depends_on('py-six@1.4.0:',   type=('build', 'run'))
    depends_on('py-pytz',         type=('build', 'run'))
    depends_on('py-tzlocal@1.2:', type=('build', 'run'))
