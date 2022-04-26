# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json

import jsonschema
import six

import llnl.util.tty as tty

import spack.cmd
import spack.hash_types as hash_types
from spack.schema.cray_manifest import schema as manifest_schema

#: Cray systems can store a Spack-compatible description of system
#: packages here.
default_path = '/opt/cray/pe/cpe-descriptive-manifest/'


def compiler_from_entry(entry):
    compiler_name = entry['name']
    paths = entry['executables']
    version = entry['version']
    arch = entry['arch']
    operating_system = arch['os']
    target = arch['target']

    compiler_cls = spack.compilers.class_for_compiler_name(compiler_name)
    spec = spack.spec.CompilerSpec(compiler_cls.name, version)
    paths = [paths.get(x, None) for x in ('cc', 'cxx', 'f77', 'fc')]
    return compiler_cls(
        spec, operating_system, target, paths
    )


def spec_from_entry(entry):
    arch_str = ""
    if 'arch' in entry:
        arch_format = "arch={platform}-{os}-{target}"
        arch_str = arch_format.format(
            platform=entry['arch']['platform'],
            os=entry['arch']['platform_os'],
            target=entry['arch']['target']['name']
        )

    compiler_str = ""
    if 'compiler' in entry:
        compiler_format  = "%{name}@{version}"
        compiler_str = compiler_format.format(
            name=entry['compiler']['name'],
            version=entry['compiler']['version']
        )

    spec_format = "{name}@{version} {compiler} {arch}"
    spec_str = spec_format.format(
        name=entry['name'],
        version=entry['version'],
        compiler=compiler_str,
        arch=arch_str
    )

    package = spack.repo.get(entry['name'])

    if 'parameters' in entry:
        variant_strs = list()
        for name, value in entry['parameters'].items():
            # TODO: also ensure that the variant value is valid?
            if not (name in package.variants):
                tty.debug("Omitting variant {0} for entry {1}/{2}"
                          .format(name, entry['name'], entry['hash'][:7]))
                continue

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

    for ht in [hash_types.dag_hash, hash_types.build_hash,
               hash_types.full_hash]:
        setattr(spec, ht.attr, entry['hash'])

    spec._concrete = True
    spec._hashes_final = True
    spec.external_path = entry['prefix']
    spec.origin = 'external-db'
    spack.spec.Spec.ensure_valid_variants(spec)

    return spec


def entries_to_specs(entries):
    spec_dict = {}
    for entry in entries:
        try:
            spec = spec_from_entry(entry)
            spec_dict[spec._hash] = spec
        except spack.repo.UnknownPackageError:
            tty.debug("Omitting package {0}: no corresponding repo package"
                      .format(entry['name']))
        except spack.error.SpackError:
            raise
        except Exception:
            tty.warn("Could not parse entry: " + str(entry))

    for entry in filter(lambda x: 'dependencies' in x, entries):
        dependencies = entry['dependencies']
        for name, properties in dependencies.items():
            dep_hash = properties['hash']
            deptypes = properties['type']
            if dep_hash in spec_dict:
                if entry['hash'] not in spec_dict:
                    continue
                parent_spec = spec_dict[entry['hash']]
                dep_spec = spec_dict[dep_hash]
                parent_spec._add_dependency(dep_spec, deptypes)

    return spec_dict


def read(path, apply_updates):
    with open(path, 'r') as json_file:
        json_data = json.load(json_file)

    jsonschema.validate(json_data, manifest_schema)

    specs = entries_to_specs(json_data['specs'])
    tty.debug("{0}: {1} specs read from manifest".format(
        path,
        str(len(specs))))
    compilers = list()
    if 'compilers' in json_data:
        compilers.extend(compiler_from_entry(x)
                         for x in json_data['compilers'])
    tty.debug("{0}: {1} compilers read from manifest".format(
        path,
        str(len(compilers))))
    if apply_updates and compilers:
        spack.compilers.add_compilers_to_config(
            compilers, init_config=False)
    if apply_updates:
        for spec in specs.values():
            spack.store.db.add(spec, directory_layout=None)
