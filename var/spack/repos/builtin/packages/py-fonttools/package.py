# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFonttools(PythonPackage):
    """fontTools is a library for manipulating fonts, written in Python.

    The project includes the TTX tool, that can convert TrueType and OpenType fonts to
    and from an XML text format, which is also called TTX. It supports TrueType,
    OpenType, AFM and to an extent Type 1 and some Mac-specific formats."""

    homepage = "https://github.com/fonttools/fonttools"
    pypi     = "fonttools/fonttools-4.28.1.zip"

    version('4.28.1', sha256='8c8f84131bf04f3b1dcf99b9763cec35c347164ab6ad006e18d2f99fcab05529')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
