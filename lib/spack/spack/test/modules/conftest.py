##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import collections
import contextlib

import cStringIO
import pytest
import spack.modules.common
from spack.util.path import canonicalize_path


@pytest.fixture()
def file_registry():
    """Fake filesystem for modulefiles test"""
    return collections.defaultdict(cStringIO.StringIO)


@pytest.fixture()
def filename_dict(file_registry, monkeypatch):
    """Returns a fake open that writes on a StringIO instance instead
    of disk.
    """
    @contextlib.contextmanager
    def _mock(filename, mode):
        if not mode == 'w':
            raise RuntimeError('opening mode must be "w" [stringio_open]')

        file_registry[filename] = cStringIO.StringIO()
        try:
            yield file_registry[filename]
        finally:
            handle = file_registry[filename]
            file_registry[filename] = handle.getvalue()
            handle.close()
    # Patch open in te appropriate module
    monkeypatch.setattr(spack.modules.common, 'open', _mock, raising=False)
    return file_registry


@pytest.fixture()
def modulefile_content(filename_dict):
    """Writes the module file and returns the content as a string.

    :param factory: module file factory
    :param spec: spec of the module file to be written
    :return: content of the module file
    :rtype: str
    """

    def _impl(factory, spec_str):
        # Write the module file
        spec = spack.spec.Spec(spec_str)
        spec.concretize()
        generator = factory(spec)
        generator.write()

        # Get its filename
        filename = generator.layout.filename
        # Retrieve the content
        content = filename_dict[filename].split('\n')
        generator.remove()
        return content

    return _impl


@pytest.fixture()
def update_template_dirs(config, monkeypatch):
    dirs = spack.config.get_config('config')['template_dirs']
    dirs = [canonicalize_path(x) for x in dirs]
    monkeypatch.setattr(spack.tengine.environment, 'template_dirs', dirs)
