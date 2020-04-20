
from pprint import pprint as pp

import collections
import collections.abc
import copy
import hashlib
import os

import spack.ci as ci
import spack.spec as spec
import spack.environment as environment
import spack.util.spack_yaml as syaml

def matches(obj, proto):
    if isinstance(obj, collections.abc.Mapping):
        if not isinstance(proto, collections.abc.Mapping):
            return False

        return all(
            (key in obj and matches(obj[key], val))
            for key, val in proto.items()
        )

    if (isinstance(obj, collections.abc.Sequence) and
            not isinstance(obj, str)):

        if not (isinstance(proto, collections.abc.Sequence) and
                not isinstance(proto, str)):
            return False

        if len(obj) != len(proto):
            return False

        return all(
            matches(obj[index], val)
            for index, val in enumerate(proto)
        )

    return obj == proto


def subkeys(obj, proto):
    if not (isinstance(obj, collections.abc.Mapping) and
            isinstance(proto, collections.abc.Mapping)):
        return obj

    new_obj = {}
    for key, value in obj.items():
        if key not in proto:
            new_obj[key] = value
            continue

        if (matches(value, proto[key]) and
            matches(proto[key], value)):
            continue

        if isinstance(value, collections.abc.Mapping):
            new_obj[key] = subkeys(value, proto[key])
            continue

        new_obj[key] = value

    return new_obj


def add_extends(yaml, key):
    has_key = ('extends' in yaml)
    extends = yaml.get('extends')

    if has_key and not isinstance(extends, (str, collections.abc.Sequence)):
        return

    if extends is None:
        yaml['extends'] = key
        return

    if isinstance(extends, str):
        if extends != key:
            yaml['extends'] = [extends, key]
        return

    if key not in extends:
        extends.append(key)


def common_subobject(yaml, sub):
    match_list = set(k for k, v in yaml.items() if matches(v, sub))

    if not match_list:
        return yaml

    common_prefix = '.c'
    common_index = 0

    while True:
        common_key = ''.join((common_prefix, str(common_index)))
        if common_key not in yaml:
            break
        common_index += 1

    new_yaml = {}

    for key, val in yaml.items():
        new_yaml[key] = copy.deepcopy(val)

        if not matches(val, sub):
            continue

        new_yaml[key] = subkeys(new_yaml[key], sub)
        add_extends(new_yaml[key], common_key)

    new_yaml[common_key] = sub

    return new_yaml, common_key


def print_delta(name, old, new, applied=None):
    delta = new - old
    reldelta = (1000*delta)//old
    reldelta = (reldelta//10, reldelta%10)

    if applied is None:
        applied = (new <= old)

    print('\n'.join((
        '{} {}:',
        '  before: {: 10d}',
        '  after : {: 10d}',
        '  delta : {:+10d} ({:=+3d}.{}%)',
    )).format(
        name,
        ('+' if applied else 'x'),
        old,
        new,
        delta,
        reldelta[0],
        reldelta[1]
    ))

def try_optimization_pass(name, yaml, optimization_pass, *args, **kwargs):
    result = optimization_pass(yaml, *args, **kwargs)
    new_yaml, other_results = result[0], result[1:]

    if new_yaml is yaml:
        # pass was not applied
        return (yaml, new_yaml, False, other_results)

    pre_size = len(syaml.dump_config(yaml, default_flow_style=True))
    post_size = len(syaml.dump_config(new_yaml, default_flow_style=True))

    # pass makes the size worse: not applying
    applied = (post_size <= pre_size)
    if applied:
        yaml, new_yaml = new_yaml, yaml

    if name:
        print_delta(name, pre_size, post_size, applied)

    return (yaml, new_yaml, applied, other_results)


def build_histogram(iterator, key):
    buckets = collections.defaultdict(int)
    values = {}

    num_objects = 0
    for obj in iterator:
        num_objects += 1

        try:
            val = obj[key]
        except (KeyError, TypeError):
            continue

        h = hashlib.sha1()
        h.update(syaml.dump_config(val).encode())
        h = h.hexdigest()

        buckets[h] += 1
        values[h] = val

    return [(h, buckets[h], float(buckets[h])/num_objects, values[h])
            for h in sorted(buckets.keys(), key=lambda k: -buckets[k])]


def optimizer(yaml):
    original_size = len(syaml.dump_config(yaml, default_flow_style=True))

    # try factoring out commonly repeated portions
    common_job = {
        'variables': {
            'SPACK_COMPILER_ACTION': 'NONE',
            'SPACK_RELATED_BUILDS_CDASH': ''
        },

        'after_script': ['rm -rf "./spack"'],

        'artifacts': {
          'paths': ['jobs_scratch_dir', 'cdash_report'],
          'when': 'always'
        },
    }

    # look for a list of tags that appear frequently
    _, count, proportion, tags = next(iter(
            build_histogram(yaml.values(), 'tags')),
            (None,)*4)

    # If a list of tags is found, and there are more than one job that uses it,
    # *and* the jobs that do use it represent at least 70% of all jobs, then add
    # the list to the prototype object.
    if tags and count > 1 and proportion >= 0.70:
        common_job['tags'] = tags

    # apply common object factorization
    yaml, other, applied, rest = try_optimization_pass(
            'general common object factorization',
            yaml, common_subobject, common_job)

    # look for a common script, and try factoring that out
    _, count, proportion, script = next(iter(
            build_histogram(yaml.values(), 'script')),
            (None,)*4)

    if script and count > 1 and proportion >= 0.70:
        yaml, other, applied, rest = try_optimization_pass(
                'script factorization',
                yaml, common_subobject, { 'script': script })

    # look for a common before_script, and try factoring that out
    _, count, proportion, script = next(iter(
            build_histogram(yaml.values(), 'before_script')),
            (None,)*4)

    if script and count > 1 and proportion >= 0.70:
        yaml, other, applied, rest = try_optimization_pass(
                'before_script factorization',
                yaml, common_subobject, { 'before_script': script })

    # Look specifically for the SPACK_ROOT_SPEC environment variables.
    # Try to factor them out.
    h = build_histogram((
        getattr(val, 'get', lambda *args: {})('variables')
        for val in yaml.values()), 'SPACK_ROOT_SPEC')

    # In this case, we try to factor out *all* instances of the SPACK_ROOT_SPEC
    # environment variable; not just the one that appears with the greatest
    # frequency. We only require that more than 1 job uses a given instance's
    # value, because we expect the value to be very large, and so expect even
    # few-to-one factorizations to yield large space savings.
    counter = 0
    for _, count, proportion, spec in h:
        if count <= 1:
            continue

        counter += 1

        yaml, other, applied, rest = try_optimization_pass(
                'SPACK_ROOT_SPEC factorization ({})'.format(counter),
                yaml,
                common_subobject,
                { 'variables': { 'SPACK_ROOT_SPEC': spec } })

    new_size = len(syaml.dump_config(yaml, default_flow_style=True))

    print('\n')
    print_delta('overall summary', original_size, new_size)
    print('\n')
    return yaml


env = environment.Environment('.')
ci.generate_gitlab_ci_yaml(
    env, True, 'test.yaml',
    custom_spack_repo='custom-repo',
    custom_spack_ref='custom-ref',
    optimizer=optimizer)
    # )

