import json
import six

import spack.cmd

from spack.spec import Spec

example_x_json_str = """\
{
  "name": "packagex",
  "hash": "hash-of-x",
  "prefix": "/path/to/packagex-install/",
  "version": "1.0",
  "arch": {
    "platform": "linux",
    "platform_os": "centos8",
    "target": {
      "name": "haswell"
    }
  },
  "compiler": {
    "name": "gcc",
    "version": "10.2.0"
  },
  "dependencies": {
    "packagey": {
      "hash": "hash-of-y",
      "type": ["link"]
    }
  },
  "parameters": {
    "precision": ["double", "float"]
  }
}
"""

class JsonSpecEntry(object):
    def __init__(self, name, hash, prefix, version, arch, compiler,
                 dependencies, parameters):
        self.name = name
        self.hash = hash
        self.prefix = prefix
        self.version = version
        self.arch = arch
        self.compiler = compiler
        self.dependencies = dependencies
        self.parameters = parameters

    def to_dict(self):
        return {
            'name': self.name,
            'hash': self.hash,
            'prefix': self.prefix,
            'version': self.version,
            'arch': self.arch,
            'compiler': self.compiler,
            'dependencies': self.dependencies,
            'parameters': self.parameters
        }

    def as_dependency(self, deptypes):
        return (self.name,
                {'hash': self.hash,
                 'type': list(deptypes)})

class JsonArchEntry(object):
    def __init__(self, platform, os, target):
        self.platform = platform
        self.os = os
        self.target = target

    def to_dict(self):
        return {
            'platform': self.platform,
            'platform_os': self.os,
            'target': {
                'name': self.target
            }
        }

class JsonCompilerEntry(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def to_dict(self):
        return {
            'name': self.name,
            'version': self.version
        }

_common_arch = JsonArchEntry(
    platform='linux',
    os='centos8',
    target='haswell'
).to_dict()

_common_compiler = JsonCompilerEntry(
    name='gcc',
    version='10.2.0'
).to_dict()

def test_compatibility():
    y = JsonSpecEntry(
        name='packagey',
        hash='hash-of-y',
        prefix='/path/to/packagey-install/',
        version='1.0',
        arch=_common_arch,
        compiler=_common_compiler,
        dependencies={},
        parameters={}
    )

    x = JsonSpecEntry(
        name='packagex',
        hash='hash-of-x',
        prefix='/path/to/packagex-install/',
        version='1.0',
        arch=_common_arch,
        compiler=_common_compiler,
        dependencies=dict([y.as_dependency(deptypes=['link'])]),
        parameters={'precision': ['double', 'float']}
    )

    x_from_entry = x.to_dict()
    x_from_str = json.loads(example_x_json_str)
    for key, val in x_from_entry.items():
        if val != x_from_str[key]:
            import pdb; pdb.set_trace()
    assert x_from_entry == x_from_str

def spec_from_entry(entry):
    arch_format = "{platform}-{os}-{target}"
    arch_str = arch_format.format(
        platform = entry['arch']['platform'],
        os = entry['arch']['platform_os'],
        target = entry['arch']['target']['name']
    )
    compiler_format  = "{name}@{version}"
    compiler_str = compiler_format.format(
        name = entry['compiler']['name'],
        version = entry['compiler']['version']
    )
    spec_format = "{name}@{version}%{compiler} arch={arch}"
    spec_str = spec_format.format(
        name = entry['name'],
        version = entry['version'],
        compiler = compiler_str,
        arch = arch_str
    )

    variants_strs = list()
    if 'parameters' in entry:
        variant_strs = list()
        for name, value in entry['parameters'].items():
            # Value could be a list (of strings), boolean, or string
            if isinstance(value, six.string_types):
                variant_strs.append('{0}={1}'.format(name, value))
            else:
                try:
                    iter(value)
                    variant_strs.append(
                        '{0}={1}'.format(name, ','.join(value)))
                    continue
                except TypeError:
                    # Not an iterable
                    pass
                # At this point not a string or collection, check for boolean
                if value in [True, False]:
                    bool_symbol = '+' if value else '~'
                    variant_strs.append('{0}{1}'.format(bool_symbol, name))
                else:
                    raise ValueError(
                        "Unexpected value for {0} ({1}): {2}".format(
                            name, str(type(value)), str(value)
                        )
                    )
        spec_str += ' ' + ' '.join(variant_strs)

    spec, = spack.cmd.parse_specs(spec_str.split())
    return spec

def generate_openmpi_entries():
    hwloc = JsonSpecEntry(
        name='hwloc',
        hash='x',
        prefix='/path/to/hwloc-install/',
        version='2.0.3',
        arch=_common_arch,
        compiler=_common_compiler,
        dependencies={},
        parameters={}
    )

    openmpi = JsonSpecEntry(
        name='openmpi',
        hash='y',
        prefix='/path/to/packagex-install/',
        version='4.1.0',
        arch=_common_arch,
        compiler=_common_compiler,
        dependencies=dict([hwloc.as_dependency(deptypes=['link'])]),
        parameters={
            'internal_hwloc': False,
            'fabrics': ['psm']
        }
    )

    return [openmpi, hwloc]

def entries_to_specs(entries):
    spec_dict = {}
    for entry in entries:
        spec = spec_from_entry(entry)
        spec._hash = entry['hash']
        spec._concrete = True
        spec.external_path = entry['prefix']
        spec_dict[entry['hash']] = spec

    for entry in entries:
        dependencies = entry['dependencies']
        for name, properties in dependencies.items():
            dep_hash = properties['hash']
            deptypes = properties['type']
            if dep_hash in spec_dict:
                parent_spec = spec_dict[entry['hash']]
                dep_spec = spec_dict[dep_hash]
                parent_spec._add_dependency(dep_spec, deptypes)

    return spec_dict

def test_spec_conversion():
    entries = list(x.to_dict() for x in generate_openmpi_entries())
    entries_to_specs(entries)

def main():
    test_compatibility()
    test_spec_conversion()

if __name__ == "__main__":
    main()
