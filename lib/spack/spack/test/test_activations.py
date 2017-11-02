##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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

import spack
from llnl.util.filesystem import join_path
from spack.directory_layout import YamlDirectoryLayout
from spack.filesystem_view import YamlFilesystemView

import os
import pytest


class FakeExtensionPackage(object):
    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix
        self.spec = FakeSpec(self)


class FakeSpec(object):
    def __init__(self, package):
        self.name = package.name
        self.prefix = package.prefix
        self.hash = self.name

    def dag_hash(self):
        return self.hash


def create_dir_structure(tmpdir, dir_structure):
    for fname, children in dir_structure.items():
        tmpdir.ensure(fname, dir=fname.endswith('/'))
        if children:
            create_dir_structure(tmpdir.join(fname), children)


@pytest.fixture()
def python_and_extension_dirs(tmpdir):
    python_dirs = {
        'bin/': {
            'python': None
        },
        'lib/': {
            'python2.7/': {
                'site-packages/': None
            }
        }
    }

    python_name = 'python'
    python_prefix = tmpdir.join(python_name)
    create_dir_structure(python_prefix, python_dirs)

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True
    python_spec.package.spec._set_test_prefix(str(python_prefix))

    ext_dirs = {
        'bin/': {
            'py-ext-tool': None
        },
        'lib/': {
            'python2.7/': {
                'site-packages/': {
                    'py-extension/': {
                        'sample.py': None
                    }
                }
            }
        }
    }

    ext_name = 'py-extension'
    ext_prefix = tmpdir.join(ext_name)
    create_dir_structure(ext_prefix, ext_dirs)

    easy_install_location = 'lib/python2.7/site-packages/easy-install.pth'
    with open(join_path(ext_prefix, easy_install_location), 'w') as F:
        F.write("""path/to/ext1.egg
path/to/setuptools.egg""")

    return str(python_prefix), str(ext_prefix)


def test_python_activation(tmpdir):
    # Note the lib directory is based partly on the python version
    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True

    python_name = 'python'
    tmpdir.ensure(python_name, dir=True)

    python_prefix = str(tmpdir.join(python_name))
    # Set the prefix on the package's spec reference because that is a copy of
    # the original spec
    python_spec.package.spec._set_test_prefix(python_prefix)

    ext_name = 'py-extension'
    tmpdir.ensure(ext_name, dir=True)
    ext_pkg = FakeExtensionPackage(ext_name, str(tmpdir.join(ext_name)))

    python_pkg = python_spec.package
    python_pkg.activate(ext_pkg)


def test_python_activation_with_files(tmpdir, python_and_extension_dirs):
    python_prefix, ext_prefix = python_and_extension_dirs

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True
    python_spec.package.spec._set_test_prefix(python_prefix)

    ext_pkg = FakeExtensionPackage('py-extension', ext_prefix)

    python_pkg = python_spec.package
    python_pkg.activate(ext_pkg)

    assert os.path.exists(join_path(python_prefix, 'bin/py-ext-tool'))

    easy_install_location = 'lib/python2.7/site-packages/easy-install.pth'
    with open(join_path(python_prefix, easy_install_location), 'r') as F:
        easy_install_contents = F.read()

    assert 'ext1.egg' in easy_install_contents
    assert 'setuptools.egg' not in easy_install_contents


def test_python_activation_view(tmpdir, python_and_extension_dirs):
    python_prefix, ext_prefix = python_and_extension_dirs

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True
    python_spec.package.spec._set_test_prefix(python_prefix)

    ext_pkg = FakeExtensionPackage('py-extension', ext_prefix)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext_pkg, extensions_layout=view.extensions_layout)

    assert not os.path.exists(join_path(python_prefix, 'bin/py-ext-tool'))

    assert os.path.exists(join_path(view_dir, 'bin/py-ext-tool'))
