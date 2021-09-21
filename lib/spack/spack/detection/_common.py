# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Common functions and data structures used by other subpackages"""
import collections
import os
import os.path

import six

import llnl.util.tty

import spack.config
import spack.spec
import spack.util.spack_yaml

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
    # Assume that prefix ends with /bin/, strip off the 'bin' directory
    # to get a Spack-compatible prefix
    assert os.path.isdir(executable_dir)
    if os.path.basename(executable_dir) == 'bin':
        return os.path.dirname(executable_dir)


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
