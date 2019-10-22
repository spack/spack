# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import functools
import platform
import re
import subprocess
import warnings

import six

from .microarchitecture import generic_microarchitecture, targets

#: Mapping from operating systems to chain of commands
#: to obtain a dictionary of raw info on the current cpu
info_factory = collections.defaultdict(list)

#: Mapping from micro-architecture families (x86_64, ppc64le, etc.) to
#: functions checking the compatibility of the host with a given target
compatibility_checks = {}


def info_dict(operating_system):
    """Decorator to mark functions that are meant to return raw info on
    the current cpu.

    Args:
        operating_system (str or tuple): operating system for which the marked
            function is a viable factory of raw info dictionaries.
    """
    def decorator(factory):
        info_factory[operating_system].append(factory)

        @functools.wraps(factory)
        def _impl():
            info = factory()

            # Check that info contains a few mandatory fields
            msg = 'field "{0}" is missing from raw info dictionary'
            assert 'vendor_id' in info, msg.format('vendor_id')
            assert 'flags' in info, msg.format('flags')
            assert 'model' in info, msg.format('model')
            assert 'model_name' in info, msg.format('model_name')

            return info

        return _impl

    return decorator


@info_dict(operating_system='Linux')
def proc_cpuinfo():
    """Returns a raw info dictionary by parsing the first entry of
    ``/proc/cpuinfo``
    """
    info = {}
    with open('/proc/cpuinfo') as file:
        for line in file:
            key, separator, value = line.partition(':')

            # If there's no separator and info was already populated
            # according to what's written here:
            #
            # http://www.linfo.org/proc_cpuinfo.html
            #
            # we are on a blank line separating two cpus. Exit early as
            # we want to read just the first entry in /proc/cpuinfo
            if separator != ':' and info:
                break

            info[key.strip()] = value.strip()
    return info


def check_output(args):
    output = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    return six.text_type(output.decode('utf-8'))


@info_dict(operating_system='Darwin')
def sysctl():
    """Returns a raw info dictionary parsing the output of sysctl."""

    info = {}
    info['vendor_id'] = check_output(
        ['sysctl', '-n', 'machdep.cpu.vendor']
    ).strip()
    info['flags'] = check_output(
        ['sysctl', '-n', 'machdep.cpu.features']
    ).strip().lower()
    info['flags'] += ' ' + check_output(
        ['sysctl', '-n', 'machdep.cpu.leaf7_features']
    ).strip().lower()
    info['model'] = check_output(
        ['sysctl', '-n', 'machdep.cpu.model']
    ).strip()
    info['model name'] = check_output(
        ['sysctl', '-n', 'machdep.cpu.brand_string']
    ).strip()

    # Super hacky way to deal with slight representation differences
    # Would be better to somehow consider these "identical"
    if 'sse4.1' in info['flags']:
        info['flags'] += ' sse4_1'
    if 'sse4.2' in info['flags']:
        info['flags'] += ' sse4_2'
    if 'avx1.0' in info['flags']:
        info['flags'] += ' avx'

    return info


def raw_info_dictionary():
    """Returns a dictionary with information on the cpu of the current host.

    This function calls all the viable factories one after the other until
    there's one that is able to produce the requested information.
    """
    info = {}
    for factory in info_factory[platform.system()]:
        try:
            info = factory()
        except Exception as e:
            warnings.warn(str(e))

        if info:
            break

    return info


def compatible_microarchitectures(info):
    """Returns an unordered list of known micro-architectures that are
    compatible with the info dictionary passed as argument.

    Args:
        info (dict): dictionary containing information on the host cpu
    """
    architecture_family = platform.machine()
    # If a tester is not registered, be conservative and assume no known
    # target is compatible with the host
    tester = compatibility_checks.get(architecture_family, lambda x, y: False)
    return [x for x in targets.values() if tester(info, x)] or \
           [generic_microarchitecture(architecture_family)]


def host():
    """Detects the host micro-architecture and returns it."""
    # Retrieve a dictionary with raw information on the host's cpu
    info = raw_info_dictionary()

    # Get a list of possible candidates for this micro-architecture
    candidates = compatible_microarchitectures(info)

    # Reverse sort of the depth for the inheritance tree among only targets we
    # can use. This gets the newest target we satisfy.
    return sorted(candidates, key=lambda t: len(t.ancestors), reverse=True)[0]


def compatibility_check(architecture_family):
    """Decorator to register a function as a proper compatibility check.

    A compatibility check function takes the raw info dictionary as a first
    argument and an arbitrary target as the second argument. It returns True
    if the target is compatible with the info dictionary, False otherwise.

    Args:
        architecture_family (str or tuple): architecture family for which
            this test can be used, e.g. x86_64 or ppc64le etc.
    """
    # Turn the argument into something iterable
    if isinstance(architecture_family, six.string_types):
        architecture_family = (architecture_family,)

    def decorator(func):
        # TODO: on removal of Python 2.6 support this can be re-written as
        # TODO: an update +  a dict comprehension
        for arch_family in architecture_family:
            compatibility_checks[arch_family] = func

        return func

    return decorator


@compatibility_check(architecture_family=('ppc64le', 'ppc64'))
def compatibility_check_for_power(info, target):
    basename = platform.machine()
    generation_match = re.search(r'POWER(\d+)', info.get('cpu', ''))
    generation = int(generation_match.group(1))

    # We can use a target if it descends from our machine type and our
    # generation (9 for POWER9, etc) is at least its generation.
    arch_root = targets[basename]
    return (target == arch_root or arch_root in target.ancestors) \
        and target.generation <= generation


@compatibility_check(architecture_family='x86_64')
def compatibility_check_for_x86_64(info, target):
    basename = 'x86_64'
    vendor = info.get('vendor_id', 'generic')
    features = set(info.get('flags', '').split())

    # We can use a target if it descends from our machine type, is from our
    # vendor, and we have all of its features
    arch_root = targets[basename]
    return (target == arch_root or arch_root in target.ancestors) \
        and (target.vendor == vendor or target.vendor == 'generic') \
        and target.features.issubset(features)
