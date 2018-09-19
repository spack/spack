##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import os
import pytest
import sys

import spack.spec
import spack.package
from llnl.util.link_tree import MergeConflictError
from spack.build_systems.python import PythonPackage
from spack.directory_layout import YamlDirectoryLayout
from spack.filesystem_view import YamlFilesystemView
from spack.util.prefix import Prefix

"""This includes tests for customized activation logic for specific packages
   (e.g. python and perl).
"""


class FakeExtensionPackage(spack.package.PackageViewMixin):
    def __init__(self, name, prefix):
        self.name = name
        self.prefix = Prefix(prefix)
        self.spec = FakeSpec(self)


class FakeSpec(object):
    def __init__(self, package):
        self.name = package.name
        self.prefix = package.prefix
        self.hash = self.name
        self.package = package
        self.concrete = True

    def dag_hash(self):
        return self.hash

    def __lt__(self, other):
        return self.name < other.name


class FakePythonExtensionPackage(FakeExtensionPackage):
    def __init__(self, name, prefix, py_namespace, python_spec):
        self.py_namespace = py_namespace
        self.extendee_spec = python_spec
        super(FakePythonExtensionPackage, self).__init__(name, prefix)

    def add_files_to_view(self, view, merge_map):
        if sys.version_info >= (3, 0):
            add_fn = PythonPackage.add_files_to_view
        else:
            add_fn = PythonPackage.add_files_to_view.im_func
        return add_fn(self, view, merge_map)

    def view_file_conflicts(self, view, merge_map):
        if sys.version_info >= (3, 0):
            conflicts_fn = PythonPackage.view_file_conflicts
        else:
            conflicts_fn = PythonPackage.view_file_conflicts.im_func
        return conflicts_fn(self, view, merge_map)

    def remove_files_from_view(self, view, merge_map):
        if sys.version_info >= (3, 0):
            remove_fn = PythonPackage.remove_files_from_view
        else:
            remove_fn = PythonPackage.remove_files_from_view.im_func
        return remove_fn(self, view, merge_map)


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
    python_spec.package.spec.prefix = str(python_prefix)

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
    with open(str(ext_prefix.join(easy_install_location)), 'w') as f:
        f.write("""path/to/ext1.egg
path/to/setuptools.egg""")

    return str(python_prefix), str(ext_prefix)


@pytest.fixture()
def namespace_extensions(tmpdir):
    ext1_dirs = {
        'bin/': {
            'py-ext-tool1': None
        },
        'lib/': {
            'python2.7/': {
                'site-packages/': {
                    'examplenamespace/': {
                        '__init__.py': None,
                        'ext1_sample.py': None
                    }
                }
            }
        }
    }

    ext2_dirs = {
        'bin/': {
            'py-ext-tool2': None
        },
        'lib/': {
            'python2.7/': {
                'site-packages/': {
                    'examplenamespace/': {
                        '__init__.py': None,
                        'ext2_sample.py': None
                    }
                }
            }
        }
    }

    ext1_name = 'py-extension1'
    ext1_prefix = tmpdir.join(ext1_name)
    create_dir_structure(ext1_prefix, ext1_dirs)

    ext2_name = 'py-extension2'
    ext2_prefix = tmpdir.join(ext2_name)
    create_dir_structure(ext2_prefix, ext2_dirs)

    return str(ext1_prefix), str(ext2_prefix), 'examplenamespace'


def test_python_activation_with_files(tmpdir, python_and_extension_dirs):
    python_prefix, ext_prefix = python_and_extension_dirs

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True
    python_spec.package.spec.prefix = python_prefix

    ext_pkg = FakeExtensionPackage('py-extension', ext_prefix)

    python_pkg = python_spec.package
    python_pkg.activate(ext_pkg, python_pkg.view())

    assert os.path.exists(os.path.join(python_prefix, 'bin/py-ext-tool'))

    easy_install_location = 'lib/python2.7/site-packages/easy-install.pth'
    with open(os.path.join(python_prefix, easy_install_location), 'r') as f:
        easy_install_contents = f.read()

    assert 'ext1.egg' in easy_install_contents
    assert 'setuptools.egg' not in easy_install_contents


def test_python_activation_view(tmpdir, python_and_extension_dirs):
    python_prefix, ext_prefix = python_and_extension_dirs

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True
    python_spec.package.spec.prefix = python_prefix

    ext_pkg = FakeExtensionPackage('py-extension', ext_prefix)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext_pkg, view)

    assert not os.path.exists(os.path.join(python_prefix, 'bin/py-ext-tool'))

    assert os.path.exists(os.path.join(view_dir, 'bin/py-ext-tool'))


def test_python_ignore_namespace_init_conflict(tmpdir, namespace_extensions):
    """Test the view update logic in PythonPackage ignores conflicting
       instances of __init__ for packages which are in the same namespace.
    """
    ext1_prefix, ext2_prefix, py_namespace = namespace_extensions

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True

    ext1_pkg = FakePythonExtensionPackage(
        'py-extension1', ext1_prefix, py_namespace, python_spec)
    ext2_pkg = FakePythonExtensionPackage(
        'py-extension2', ext2_prefix, py_namespace, python_spec)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext1_pkg, view)
    # Normally handled by Package.do_activate, but here we activate directly
    view.extensions_layout.add_extension(python_spec, ext1_pkg.spec)
    python_pkg.activate(ext2_pkg, view)

    f1 = 'lib/python2.7/site-packages/examplenamespace/ext1_sample.py'
    f2 = 'lib/python2.7/site-packages/examplenamespace/ext2_sample.py'
    init_file = 'lib/python2.7/site-packages/examplenamespace/__init__.py'

    assert os.path.exists(os.path.join(view_dir, f1))
    assert os.path.exists(os.path.join(view_dir, f2))
    assert os.path.exists(os.path.join(view_dir, init_file))


def test_python_keep_namespace_init(tmpdir, namespace_extensions):
    """Test the view update logic in PythonPackage keeps the namespace
       __init__ file as long as one package in the namespace still
       exists.
    """
    ext1_prefix, ext2_prefix, py_namespace = namespace_extensions

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True

    ext1_pkg = FakePythonExtensionPackage(
        'py-extension1', ext1_prefix, py_namespace, python_spec)
    ext2_pkg = FakePythonExtensionPackage(
        'py-extension2', ext2_prefix, py_namespace, python_spec)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext1_pkg, view)
    # Normally handled by Package.do_activate, but here we activate directly
    view.extensions_layout.add_extension(python_spec, ext1_pkg.spec)
    python_pkg.activate(ext2_pkg, view)
    view.extensions_layout.add_extension(python_spec, ext2_pkg.spec)

    f1 = 'lib/python2.7/site-packages/examplenamespace/ext1_sample.py'
    init_file = 'lib/python2.7/site-packages/examplenamespace/__init__.py'

    python_pkg.deactivate(ext1_pkg, view)
    view.extensions_layout.remove_extension(python_spec, ext1_pkg.spec)

    assert not os.path.exists(os.path.join(view_dir, f1))
    assert os.path.exists(os.path.join(view_dir, init_file))

    python_pkg.deactivate(ext2_pkg, view)
    view.extensions_layout.remove_extension(python_spec, ext2_pkg.spec)

    assert not os.path.exists(os.path.join(view_dir, init_file))


def test_python_namespace_conflict(tmpdir, namespace_extensions):
    """Test the view update logic in PythonPackage reports an error when two
       python extensions with different namespaces have a conflicting __init__
       file.
    """
    ext1_prefix, ext2_prefix, py_namespace = namespace_extensions
    other_namespace = py_namespace + 'other'

    python_spec = spack.spec.Spec('python@2.7.12')
    python_spec._concrete = True

    ext1_pkg = FakePythonExtensionPackage(
        'py-extension1', ext1_prefix, py_namespace, python_spec)
    ext2_pkg = FakePythonExtensionPackage(
        'py-extension2', ext2_prefix, other_namespace, python_spec)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    python_pkg = python_spec.package
    python_pkg.activate(ext1_pkg, view)
    view.extensions_layout.add_extension(python_spec, ext1_pkg.spec)
    with pytest.raises(MergeConflictError):
        python_pkg.activate(ext2_pkg, view)


@pytest.fixture()
def perl_and_extension_dirs(tmpdir):
    perl_dirs = {
        'bin/': {
            'perl': None
        },
        'lib/': {
            'site_perl/': {
                '5.24.1/': {
                    'x86_64-linux/': None
                }
            }
        }
    }

    perl_name = 'perl'
    perl_prefix = tmpdir.join(perl_name)
    create_dir_structure(perl_prefix, perl_dirs)

    perl_spec = spack.spec.Spec('perl@5.24.1')
    perl_spec._concrete = True
    perl_spec.package.spec.prefix = str(perl_prefix)

    ext_dirs = {
        'bin/': {
            'perl-ext-tool': None
        },
        'lib/': {
            'site_perl/': {
                '5.24.1/': {
                    'x86_64-linux/': {
                        'TestExt/': {
                        }
                    }
                }
            }
        }
    }

    ext_name = 'perl-extension'
    ext_prefix = tmpdir.join(ext_name)
    create_dir_structure(ext_prefix, ext_dirs)

    return str(perl_prefix), str(ext_prefix)


def test_perl_activation(tmpdir):
    # Note the lib directory is based partly on the perl version
    perl_spec = spack.spec.Spec('perl@5.24.1')
    perl_spec._concrete = True

    perl_name = 'perl'
    tmpdir.ensure(perl_name, dir=True)

    perl_prefix = str(tmpdir.join(perl_name))
    # Set the prefix on the package's spec reference because that is a copy of
    # the original spec
    perl_spec.package.spec.prefix = perl_prefix

    ext_name = 'perl-extension'
    tmpdir.ensure(ext_name, dir=True)
    ext_pkg = FakeExtensionPackage(ext_name, str(tmpdir.join(ext_name)))

    perl_pkg = perl_spec.package
    perl_pkg.activate(ext_pkg, perl_pkg.view())


def test_perl_activation_with_files(tmpdir, perl_and_extension_dirs):
    perl_prefix, ext_prefix = perl_and_extension_dirs

    perl_spec = spack.spec.Spec('perl@5.24.1')
    perl_spec._concrete = True
    perl_spec.package.spec.prefix = perl_prefix

    ext_pkg = FakeExtensionPackage('perl-extension', ext_prefix)

    perl_pkg = perl_spec.package
    perl_pkg.activate(ext_pkg, perl_pkg.view())

    assert os.path.exists(os.path.join(perl_prefix, 'bin/perl-ext-tool'))


def test_perl_activation_view(tmpdir, perl_and_extension_dirs):
    perl_prefix, ext_prefix = perl_and_extension_dirs

    perl_spec = spack.spec.Spec('perl@5.24.1')
    perl_spec._concrete = True
    perl_spec.package.spec.prefix = perl_prefix

    ext_pkg = FakeExtensionPackage('perl-extension', ext_prefix)

    view_dir = str(tmpdir.join('view'))
    layout = YamlDirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)

    perl_pkg = perl_spec.package
    perl_pkg.activate(ext_pkg, view)

    assert not os.path.exists(os.path.join(perl_prefix, 'bin/perl-ext-tool'))

    assert os.path.exists(os.path.join(view_dir, 'bin/perl-ext-tool'))
