# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import re
import subprocess
import sys


# Tuple of name, flags added, flags removed (default [])
_intel_32 = [
    ('i686', []),
    ('pentium2', ['mmx']),
    ('pentium3', ['sse']),
    ('pentium4', ['sse2']),
    ('prescott', ['sse3']),
    ]

_intel_64 = [ # commenting out the ones that aren't shown through sysctl
    ('nocona', ['mmx', 'sse', 'sse2', 'sse3']),#lm
    ('core2', ['ssse3'], ['sse3']),
    ('nehalem', ['sse4_1', 'sse4_2', 'popcnt']),
    ('westmere', ['aes', 'pclmulqdq']),
    ('sandybridge', ['avx']),
    ('ivybridge', ['rdrand', 'f16c']),#fsgsbase (is it RDWRFSGS on darwin?)
    ('haswell', ['movbe', 'fma', 'avx2', 'bmi1', 'bmi2']),
    ('broadwell', ['rdseed', 'adx']),
    ('skylake', ['xsavec', 'xsaves'])
    ]

# We will need to build on these and combine with names when intel releases
# further avx512 processors.
# _intel_avx12 = ['avx512f', 'avx512cd']


_amd_10_names = [
    ('barcelona', ['mmx', 'sse', 'sse2', 'sse3', 'sse4a', 'abm'])
    ]

_amd_14_names = [
    ('btver1', ['mmx', 'sse', 'sse2', 'sse3', 'ssse3', 'sse4a', 'cx16',
                'abm']),#lm
    ]

_amd_15_names = [
    ('bdver1', ['avx', 'aes', 'pclmulqdq', 'cx16', 'sse', 'sse2', 'sse3',
                'ssse3', 'sse4a', 'sse4_1', 'sse4_2', 'abm']),#xop, lwp
    ('bdver2', ['bmi1', 'f16c', 'fma',]),#tba?
    ('bdver3', ['fsgsbase']),
    ('bdver4', ['bmi2', 'movbe', 'avx2'])
    ]

_amd_16_names = [
    ('btver2', ['mmx', 'sse', 'sse2', 'sse3', 'ssse3', 'sse4a', 'cx16',
                'abm', 'movbe', 'f16c', 'bmi1', 'avx', 'pclmulqdq',
                'aes', 'sse4_1', 'sse4_2']),#lm
    ]

_amd_17_names = [
    ('znver1', ['bmi1', 'bmi2', 'f16c', 'fma', 'fsgsbase', 'avx', 'avx2',
                'rdseed', 'mwaitx', 'clzero', 'aes', 'pclmulqdq', 'cx16',
                'movbe', 'mmx', 'sse', 'sse2', 'sse3', 'ssse3', 'sse4a',
                'sse4_1', 'sse4_2', 'abm', 'xsavec', 'xsaves',
                'clflushopt', 'popcnt', 'adcx'])
    ]

_amd_numbers = {
    0x10: _amd_10_names,
    0x14: _amd_14_names,
    0x15: _amd_15_names,
    0x16: _amd_16_names,
    0x17: _amd_17_names
    }

def supported_target_names():
    intel_names = set(t[0] for t in _intel_64)
    intel_names |= set(t[0] for t in _intel_32)
    amd_names = set()
    for family in _amd_numbers:
        amd_names |= set(t[0] for t in _amd_numbers[family])
    power_names = set('power' + str(d) for d in range(7, 10))
    return intel_names | amd_names | power_names

def create_dict_from_cpuinfo():
    # Initialize cpuinfo from file
    cpuinfo = {}
    try:
        with open('/proc/cpuinfo') as file:
            text = file.readlines()
            for line in text:
                if line.strip():
                    key, _, value = line.partition(':')
                    cpuinfo[key.strip()] = value.strip()
    except IOError:
        return None
    return cpuinfo

def check_output(args):
    if sys.version_info >= (3, 0):
        return subprocess.run(args, check=True, stdout=PIPE).stdout # nopyqver
    else:
        return subprocess.check_output(args) # nopyqver

def create_dict_from_sysctl():
    cpuinfo = {}
    try:
        cpuinfo['vendor_id'] = check_output(['sysctl', '-n',
                                  'machdep.cpu.vendor']).strip()
        cpuinfo['flags'] = check_output(['sysctl', '-n',
                                 'machdep.cpu.features']).strip().lower()
        cpuinfo['flags'] += ' ' + check_output(['sysctl', '-n',
                                 'machdep.cpu.leaf7_features']).strip().lower()
        cpuinfo['model'] = check_output(['sysctl', '-n',
                                         'machdep.cpu.model']).strip()
        cpuinfo['model name'] = check_output(['sysctl', '-n',
                                          'machdep.cpu.brand_string']).strip()

        # Super hacky way to deal with slight representation differences
        # Would be better to somehow consider these "identical"
        if 'sse4.1' in cpuinfo['flags']:
            cpuinfo['flags'] += ' sse4_1'
        if 'sse4.2' in cpuinfo['flags']:
            cpuinfo['flags'] += ' sse4_2'
        if 'avx1.0' in cpuinfo['flags']:
            cpuinfo['flags'] += ' avx'
    except:
        pass
    return cpuinfo

def get_cpu_name():
    name = get_cpu_name_helper(platform.system())
    return name if name else platform.machine()

def get_cpu_name_helper(system):
    # TODO: Elsewhere create dict of codenames (targets) and flag sets.
    # Return cpu name or an empty string if one cannot be determined.
    cpuinfo = {}
    if system == 'Linux':
        cpuinfo = create_dict_from_cpuinfo()
    elif system == 'Darwin':
        cpuinfo = create_dict_from_sysctl()
    if not cpuinfo:
        return ''

    if 'vendor_id' in cpuinfo and cpuinfo['vendor_id'] == 'GenuineIntel':
        if 'model name' not in cpuinfo or 'flags' not in cpuinfo:
            # We don't have the information we need to determine the
            # microarchitecture name
            return ''
        return get_intel_cpu_name(cpuinfo)
    elif 'vendor_id' in cpuinfo and cpuinfo['vendor_id'] == 'AuthenticAMD':
        if 'cpu family' not in cpuinfo or 'flags' not in cpuinfo:
            # We don't have the information we need to determine the
            # microarchitecture name
            return ''
        return get_amd_cpu_name(cpuinfo)
    elif 'cpu' in cpuinfo and 'POWER' in cpuinfo['cpu']:
        return get_ibm_cpu_name(cpuinfo['cpu'])
    else:
        return ''

def get_ibm_cpu_name(cpu):
    power_pattern = re.compile('POWER(\d+)')
    power_match = power_pattern.search(cpu)
    if power_match:
        if 'le' in platform.machine():
            return 'power' + power_match.group(1) + 'le'
        return 'power' + power_match.group(1)
    else:
        return ''

def get_intel_cpu_name(cpuinfo):
    model_name = cpuinfo['model name']
    if 'Atom' in model_name:
        return 'atom'
    elif 'Quark' in model_name:
        return 'quark'
    elif 'Xeon' in model_name and 'Phi' in model_name:
        # This is hacky and needs to be extended for newer avx512 chips
        return 'knl'
    else:
        ret = ''
        flag_list = cpuinfo['flags'].split()
        proc_flags = []
        for _intel_processors in [_intel_32, _intel_64]:
            for entry in _intel_processors:
                try:
                    proc, flags_added, flags_removed = entry
                except ValueError:
                    proc, flags_added = entry
                    flags_removed = []
                proc_flags = list(filter(lambda x: x not in flags_removed, proc_flags))
                proc_flags.extend(flags_added)
                if all(f in flag_list for f in proc_flags):
                    ret = proc
        return ret

def get_amd_cpu_name(cpuinfo):
    #TODO: Learn what the "canonical" granularity of naming
    # is for AMD processors, implement dict as for intel.
    ret = ''
    flag_list = cpuinfo['flags'].split()
    model_number = int(cpuinfo['cpu family'])
    flags_dict = _amd_numbers[model_number]
    proc_flags = []
    for proc, proc_flags_added in flags_dict:
        proc_flags.extend(proc_flags_added)
        if all(f in flag_list for f in proc_flags):
            ret = proc
        else:
            break
    return ret

"""IDEA: In build_environment.setup_compiler_environment, include a
call to compiler.tuning_flags(spec.architecture.target). For gcc this
would return "-march=%s" % str(spec.architecture.target). We only call
this if the target is a valid tuning target (I.e. not
platform.machine(), but a more specific target we successfully
discovered.

Then set
SPACK_TUNING_FLAGS=compiler.tuning_flags(spec.architecture.target)
This way the compiler wrapper can just add $SPACK_TUNING_FLAGS to the
eventual command."""
