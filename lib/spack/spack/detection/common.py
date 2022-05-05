# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Define a common data structure to represent external packages and a
function to update packages.yaml given a list of detected packages.

Ideally, each detection method should be placed in a specific subpackage
and implement at least a function that returns a list of DetectedPackage
objects. The update in packages.yaml can then be done using the function
provided here.

The module also contains other functions that might be useful across different
detection mechanisms.
"""
import collections
import itertools
import os
import os.path
import re
import sys

import six

import llnl.util.tty

import spack.config
import spack.spec
import spack.util.spack_yaml

is_windows = sys.platform == 'win32'
#: Information on a package that has been detected
DetectedPackage = collections.namedtuple(
    'DetectedPackage', ['spec', 'prefix']
)


def _externals_in_packages_yaml():
    """Return all the specs mentioned as externals in packages.yaml"""
    packages_yaml = spack.config.get('packages')
    already_defined_specs = set()
    for pkg_name, package_configuration in packages_yaml.items():
        for item in package_configuration.get('externals', []):
            already_defined_specs.add(spack.spec.Spec(item['spec']))
    return already_defined_specs


def _pkg_config_dict(external_pkg_entries):
    """Generate a package specific config dict according to the packages.yaml schema.

    This does not generate the entire packages.yaml. For example, given some
    external entries for the CMake package, this could return::

        {
            'externals': [{
                'spec': 'cmake@3.17.1',
                'prefix': '/opt/cmake-3.17.1/'
            }, {
                'spec': 'cmake@3.16.5',
                'prefix': '/opt/cmake-3.16.5/'
            }]
       }
    """
    pkg_dict = spack.util.spack_yaml.syaml_dict()
    pkg_dict['externals'] = []
    for e in external_pkg_entries:
        if not _spec_is_valid(e.spec):
            continue

        external_items = [('spec', str(e.spec)), ('prefix', e.prefix)]
        if e.spec.external_modules:
            external_items.append(('modules', e.spec.external_modules))

        if e.spec.extra_attributes:
            external_items.append(
                ('extra_attributes',
                 spack.util.spack_yaml.syaml_dict(e.spec.extra_attributes.items()))
            )

        # external_items.extend(e.spec.extra_attributes.items())
        pkg_dict['externals'].append(
            spack.util.spack_yaml.syaml_dict(external_items)
        )

    return pkg_dict


def _spec_is_valid(spec):
    try:
        str(spec)
    except spack.error.SpackError:
        # It is assumed here that we can at least extract the package name from
        # the spec so we can look up the implementation of
        # determine_spec_details
        msg = 'Constructed spec for {0} does not have a string representation'
        llnl.util.tty.warn(msg.format(spec.name))
        return False

    try:
        spack.spec.Spec(str(spec))
    except spack.error.SpackError:
        llnl.util.tty.warn(
            'Constructed spec has a string representation but the string'
            ' representation does not evaluate to a valid spec: {0}'
            .format(str(spec))
        )
        return False

    return True


def is_executable(file_path):
    """Return True if the path passed as argument is that of an executable"""
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)


def _convert_to_iterable(single_val_or_multiple):
    x = single_val_or_multiple
    if x is None:
        return []
    elif isinstance(x, six.string_types):
        return [x]
    elif isinstance(x, spack.spec.Spec):
        # Specs are iterable, but a single spec should be converted to a list
        return [x]

    try:
        iter(x)
        return x
    except TypeError:
        return [x]


def executable_prefix(executable_dir):
    """Given a directory where an executable is found, guess the prefix
    (i.e. the "root" directory of that installation) and return it.

    Args:
        executable_dir: directory where an executable is found
    """
    # Given a prefix where an executable is found, assuming that prefix
    # contains /bin/, strip off the 'bin' directory to get a Spack-compatible
    # prefix
    assert os.path.isdir(executable_dir)

    components = executable_dir.split(os.sep)
    if 'bin' not in components:
        return executable_dir
    idx = components.index('bin')
    return os.sep.join(components[:idx])


def library_prefix(library_dir):
    """Given a directory where an library is found, guess the prefix
    (i.e. the "root" directory of that installation) and return it.

    Args:
        library_dir: directory where an library is found
    """
    # Given a prefix where an library is found, assuming that prefix
    # contains /lib/ or /lib64/, strip off the 'lib' or 'lib64' directory
    # to get a Spack-compatible prefix
    assert os.path.isdir(library_dir)

    components = library_dir.split(os.sep)
    if 'lib64' in components:
        idx = components.index('lib64')
        return os.sep.join(components[:idx])
    elif 'lib' in components:
        idx = components.index('lib')
        return os.sep.join(components[:idx])
    else:
        return library_dir


def update_configuration(detected_packages, scope=None, buildable=True):
    """Add the packages passed as arguments to packages.yaml

    Args:
        detected_packages (list): list of DetectedPackage objects to be added
        scope (str): configuration scope where to add the detected packages
        buildable (bool): whether the detected packages are buildable or not
    """
    predefined_external_specs = _externals_in_packages_yaml()
    pkg_to_cfg, all_new_specs = {}, []
    for package_name, entries in detected_packages.items():
        new_entries = [
            e for e in entries if (e.spec not in predefined_external_specs)
        ]

        pkg_config = _pkg_config_dict(new_entries)
        all_new_specs.extend([
            spack.spec.Spec(x['spec']) for x in pkg_config.get('externals', [])
        ])
        if buildable is False:
            pkg_config['buildable'] = False
        pkg_to_cfg[package_name] = pkg_config

    pkgs_cfg = spack.config.get('packages', scope=scope)

    pkgs_cfg = spack.config.merge_yaml(pkgs_cfg, pkg_to_cfg)
    spack.config.set('packages', pkgs_cfg, scope=scope)

    return all_new_specs


def find_win32_additional_install_paths():
    """Not all programs on Windows live on the PATH
    Return a list of other potential install locations.
    """
    windows_search_ext = []
    cuda_re = r'CUDA_PATH[a-zA-Z1-9_]*'
    # The list below should be expanded with other
    # common Windows install locations as neccesary
    path_ext_keys = ['I_MPI_ONEAPI_ROOT',
                     'MSMPI_BIN',
                     'MLAB_ROOT',
                     'NUGET_PACKAGES']
    user = os.environ["USERPROFILE"]
    add_path = lambda key: re.search(cuda_re, key) or key in path_ext_keys
    windows_search_ext.extend([os.environ[key] for key
                              in os.environ.keys() if
                              add_path(key)])
    # note windows paths are fine here as this method should only ever be invoked
    # to interact with Windows
    # Add search path for default Chocolatey (https://github.com/chocolatey/choco)
    # install directory
    windows_search_ext.append("C:\\ProgramData\\chocolatey\\bin")
    # Add search path for NuGet package manager default install location
    windows_search_ext.append(os.path.join(user, ".nuget", "packages"))
    windows_search_ext.extend(
        spack.config.get("config:additional_external_search_paths", default=[])
    )
    windows_search_ext.extend(spack.util.environment.get_path('PATH'))
    return windows_search_ext


def compute_windows_program_path_for_package(pkg):
    """Given a package, attempt to compute its Windows
    program files location, return list of best guesses

    Args:
        pkg (spack.package.PackageBase): package for which
                           Program Files location is to be computed
    """
    if not is_windows:
        return []
    # note windows paths are fine here as this method should only ever be invoked
    # to interact with Windows
    program_files = 'C:\\Program Files{}\\{}'

    return[program_files.format(arch, name) for
           arch, name in itertools.product(("", " (x86)"),
           (pkg.name, pkg.name.capitalize()))]
