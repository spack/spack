# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import re
import shutil

import llnl.util.tty as tty
from llnl.util.filesystem import (
    filter_file,
    find,
    is_nonsymlink_exe_with_shebang,
    path_contains_subdirectory,
    same_path,
    working_dir,
)
from llnl.util.lang import match_predicate

from spack.directives import depends_on, extends
from spack.package import PackageBase, run_after


class PythonPackage(PackageBase):
    """Specialized class for packages that are built using pip."""
    #: Package name, version, and extension on PyPI
    pypi = None

    maintainers = ['adamjstewart']

    # Default phases
    phases = ['install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'PythonPackage'

    #: Callback names for install-time test
    install_time_test_callbacks = ['test']

    extends('python')
    depends_on('py-pip', type='build')
    # FIXME: technically wheel is only needed when building from source, not when
    # installing a downloaded wheel, but I don't want to add wheel as a dep to every
    # package manually
    depends_on('py-wheel', type='build')

    py_namespace = None

    @staticmethod
    def _std_args(cls):
        return [
            # Verbose
            '-vvv',
            # Disable prompting for input
            '--no-input',
            # Disable the cache
            '--no-cache-dir',
            # Don't check to see if pip is up-to-date
            '--disable-pip-version-check',
            # Install packages
            'install',
            # Don't install package dependencies
            '--no-deps',
            # Overwrite existing packages
            '--ignore-installed',
            # Use env vars like PYTHONPATH
            '--no-build-isolation',
            # Don't warn that prefix.bin is not in PATH
            '--no-warn-script-location',
            # Ignore the PyPI package index
            '--no-index',
        ]

    @property
    def homepage(self):
        if self.pypi:
            name = self.pypi.split('/')[0]
            return 'https://pypi.org/project/' + name + '/'

    @property
    def url(self):
        if self.pypi:
            return (
                'https://files.pythonhosted.org/packages/source/'
                + self.pypi[0] + '/' + self.pypi
            )

    @property
    def list_url(self):
        if self.pypi:
            name = self.pypi.split('/')[0]
            return 'https://pypi.org/simple/' + name + '/'

    @property
    def import_modules(self):
        """Names of modules that the Python package provides.

        These are used to test whether or not the installation succeeded.
        These names generally come from running:

        .. code-block:: python

           >> import setuptools
           >> setuptools.find_packages()

        in the source tarball directory. If the module names are incorrectly
        detected, this property can be overridden by the package.

        Returns:
            list: list of strings of module names
        """
        modules = []
        pkg = self.spec['python'].package

        # Packages may be installed in platform-specific or platform-independent
        # site-packages directories
        for directory in {pkg.platlib, pkg.purelib}:
            root = os.path.join(self.prefix, directory)

            # Some Python libraries are packages: collections of modules
            # distributed in directories containing __init__.py files
            for path in find(root, '__init__.py', recursive=True):
                modules.append(path.replace(root + os.sep, '', 1).replace(
                    os.sep + '__init__.py', '').replace('/', '.'))

            # Some Python libraries are modules: individual *.py files
            # found in the site-packages directory
            for path in find(root, '*.py', recursive=False):
                modules.append(path.replace(root + os.sep, '', 1).replace(
                    '.py', '').replace('/', '.'))

        modules = [mod for mod in modules if re.match('[a-zA-Z0-9._]+$', mod)]

        tty.debug('Detected the following modules: {0}'.format(modules))

        return modules

    @property
    def build_directory(self):
        """The root directory of the Python package.

        This is usually the directory containing one of the following files:

        * ``pyproject.toml``
        * ``setup.cfg``
        * ``setup.py``
        """
        return self.stage.source_path

    def install_options(self, spec, prefix):
        """Extra arguments to be supplied to the setup.py install command."""
        return []

    def global_options(self, spec, prefix):
        """Extra global options to be supplied to the setup.py call before the install
        or bdist_wheel command."""
        return []

    def install(self, spec, prefix):
        """Install everything from build directory."""

        args = PythonPackage._std_args(self) + ['--prefix=' + prefix]

        for option in self.install_options(spec, prefix):
            args.append('--install-option=' + option)
        for option in self.global_options(spec, prefix):
            args.append('--global-option=' + option)

        if self.stage.archive_file and self.stage.archive_file.endswith('.whl'):
            args.append(self.stage.archive_file)
        else:
            args.append('.')

        pip = inspect.getmodule(self).pip
        with working_dir(self.build_directory):
            pip(*args)

    # Testing

    def test(self):
        """Attempts to import modules of the installed package."""

        # Make sure we are importing the installed modules,
        # not the ones in the source directory
        for module in self.import_modules:
            self.run_test(inspect.getmodule(self).python.path,
                          ['-c', 'import {0}'.format(module)],
                          purpose='checking import of {0}'.format(module),
                          work_dir='spack-test')

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

    def view_file_conflicts(self, view, merge_map):
        """Report all file conflicts, excepting special cases for python.
           Specifically, this does not report errors for duplicate
           __init__.py files for packages in the same namespace.
        """
        conflicts = list(dst for src, dst in merge_map.items()
                         if os.path.exists(dst))

        if conflicts and self.py_namespace:
            ext_map = view.extensions_layout.extension_map(self.extendee_spec)
            namespaces = set(
                x.package.py_namespace for x in ext_map.values())
            namespace_re = (
                r'site-packages/{0}/__init__.py'.format(self.py_namespace))
            find_namespace = match_predicate(namespace_re)
            if self.py_namespace in namespaces:
                conflicts = list(
                    x for x in conflicts if not find_namespace(x))

        return conflicts

    def add_files_to_view(self, view, merge_map):
        bin_dir = self.spec.prefix.bin
        python_prefix = self.extendee_spec.prefix
        python_is_external = self.extendee_spec.external
        global_view = same_path(python_prefix, view.get_projection_for_spec(
            self.spec
        ))
        for src, dst in merge_map.items():
            if os.path.exists(dst):
                continue
            elif global_view or not path_contains_subdirectory(src, bin_dir):
                view.link(src, dst)
            elif not os.path.islink(src):
                shutil.copy2(src, dst)
                is_script = is_nonsymlink_exe_with_shebang(src)
                if is_script and not python_is_external:
                    filter_file(
                        python_prefix, os.path.abspath(
                            view.get_projection_for_spec(self.spec)), dst
                    )
            else:
                orig_link_target = os.path.realpath(src)
                new_link_target = os.path.abspath(merge_map[orig_link_target])
                view.link(new_link_target, dst)

    def remove_files_from_view(self, view, merge_map):
        ignore_namespace = False
        if self.py_namespace:
            ext_map = view.extensions_layout.extension_map(self.extendee_spec)
            remaining_namespaces = set(
                spec.package.py_namespace for name, spec in ext_map.items()
                if name != self.name)
            if self.py_namespace in remaining_namespaces:
                namespace_init = match_predicate(
                    r'site-packages/{0}/__init__.py'.format(self.py_namespace))
                ignore_namespace = True

        bin_dir = self.spec.prefix.bin
        global_view = (
            self.extendee_spec.prefix == view.get_projection_for_spec(
                self.spec
            )
        )

        to_remove = []
        for src, dst in merge_map.items():
            if ignore_namespace and namespace_init(dst):
                continue

            if global_view or not path_contains_subdirectory(src, bin_dir):
                to_remove.append(dst)
            else:
                os.remove(dst)

        view.remove_files(to_remove)
