import json

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

def test_compatibility():
    common_arch = JsonArchEntry(
        platform='linux',
        os='centos8',
        target='haswell'
    ).to_dict()

    common_compiler = JsonCompilerEntry(
        name='gcc',
        version='10.2.0'
    ).to_dict()

    y = JsonSpecEntry(
        name='packagey',
        hash='hash-of-y',
        prefix='/path/to/packagey-install/',
        version='1.0',
        arch=common_arch,
        compiler=common_compiler,
        dependencies={},
        parameters={}
    )

    x = JsonSpecEntry(
        name='packagex',
        hash='hash-of-x',
        prefix='/path/to/packagex-install/',
        version='1.0',
        arch=common_arch,
        compiler=common_compiler,
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
    return spec_str

def main():
    test_compatibility()

if __name__ == "__main__":
    main()
