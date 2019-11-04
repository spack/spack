# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIcs(PythonPackage):
    """Ics.py : iCalendar for Humans

    Ics.py is a pythonic and easy iCalendar library. Its goals are to
    read and write ics data in a developer friendly way.

    iCalendar is a widely-used and useful format but not user friendly.
    Ics.py is there to give you the ability of creating and reading
    this format without any knowledge of it.

    It should be able to parse every calendar that respects the
    rfc5545 and maybe some more. It also outputs rfc compliant
    calendars.

    iCalendar (file extension .ics) is used by Google Calendar, Apple
    Calendar, Android and many more.

    Ics.py is available for Python>=3.6 and is Apache2 Licensed.
    """

    homepage = "https://github.com/C4ptainCrunch/ics.py"
    git      = "git@github.com:C4ptainCrunch/ics.py.git"

    # for some reason only a .egg version is published on pypi and
    # github's archive link doesn't fetch for some reason, so use
    # the commit for the associated release
    version('0.6', commit='74d7b24cb1639d2cd027e502d5f16ea68b5e5b12')
    version('0.5', commit='8ac7db18d365d74ce6524a441a4c4548df3349ee')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-arrow@0.11:0.14.99', type=('build', 'run'))
    depends_on('py-six@1.5:', type=('build', 'run'))
    depends_on('py-tatsu@4.2:', type=('build', 'run'), when='@0.6:')
