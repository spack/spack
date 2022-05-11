# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyFonttools(PythonPackage):
    """fontTools is a library for manipulating fonts, written in Python.

    The project includes the TTX tool, that can convert TrueType and OpenType fonts to
    and from an XML text format, which is also called TTX. It supports TrueType,
    OpenType, AFM and to an extent Type 1 and some Mac-specific formats."""

    homepage = "https://github.com/fonttools/fonttools"
    pypi     = "fonttools/fonttools-4.28.1.zip"

    version('4.31.2', sha256='236b29aee6b113e8f7bee28779c1230a86ad2aac9a74a31b0aedf57e7dfb62a4')
    version('4.29.1', sha256='2b18a172120e32128a80efee04cff487d5d140fe7d817deb648b2eee023a40e4')
    version('4.28.1', sha256='8c8f84131bf04f3b1dcf99b9763cec35c347164ab6ad006e18d2f99fcab05529')
    version('4.26.2', sha256='c1c0e03dd823e9e905232e875ea02dbb2dcd2ba195418c6d11bfaea49b9c774d')

    depends_on('python@3.7:', when='@4.28:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    @property
    def import_modules(self):
        modules = super(__class__, self).import_modules

        ignored_imports = ["fontTools.ufoLib"]

        return [i for i in modules
                if not any(map(i.startswith, ignored_imports))]
