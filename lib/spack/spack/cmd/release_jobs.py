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
import re

import subprocess
from jsonschema import validate
from six import iteritems

import llnl.util.tty as tty

from spack.dependency import all_deptypes
from spack.spec import Spec
from spack.paths import spack_root
from spack.error import SpackError
from spack.schema.os_container_mapping import schema
from spack.util.spec_set import CombinatorialSpecSet
import spack.util.spack_yaml as syaml

description = "generate release build set as .gitlab-ci.yml"
section = "build"
level = "long"


IGNORE_SURROUND_REGEX = re.compile('<BEGIN_SPACK_COMMAND_OUTPUT>(.+)<END_SPACK_COMMAND_OUTPUT>', re.MULTILINE|re.DOTALL)
DEP_LINE_REGEX = re.compile('^([^\s]+) -> (.+)$', re.MULTILINE)
SPEC_LINE_REGEX = re.compile('^label: ([^,]+), spec: (.+)$', re.MULTILINE)


def setup_parser(subparser):
    subparser.add_argument(
        '-s', '--spec-set', default=None,
        help="path to release spec-set yaml file")

    subparser.add_argument(
        '-m', '--mirror-url', default='http://172.17.0.1:8081/',
        help="url of binary mirror where builds should be pushed")

    subparser.add_argument(
        '-o', '--output-file', default=".gitlab-ci.yml",
        help="path to output file to write")

    subparser.add_argument(
        '-t', '--shared-runner-tag', default=None,
        help="tag to add to jobs for shared runner selection")

    subparser.add_argument(
        '-k', '--signing-key', default=None,
        help="hash of gpg key to use for package signing")

    subparser.add_argument(
        '-c', '--cdash-url', default='https://cdash.spack.io',
        help="Base url of CDash instance jobs should communicate with")

    subparser.add_argument(
        '-p', '--print-summary', action='store_true', default=False,
        help="Print summary of staged jobs to standard output")

    subparser.add_argument(
        '--spec-deps', default=None,
        help="The spec for which you want container-generated deps")


def get_job_name(spec, osarch):
    return '{0} {1} {2} {3}'.format(spec.name, spec.version,
                                    spec.compiler, osarch)
    # return '{0}'.format(spec.short_spec)
    # return '{0} / {1}'.format(spec.short_spec, osarch)


def get_spec_string(spec):
    return '{0}@{1}%{2} arch={3}'.format(spec.name, spec.version,
                                         spec.compiler, spec.architecture)


def get_deps_using_container(spec, container_info, deps, spec_labels):
    image = container_info['image']

    cmd_to_run = [
        'docker', 'run', '--rm',
        '-v', '{0}:/home/scott/spack'.format(spack_root),
        '--entrypoint', '/home/scott/spackcommand/spack-container-command.sh',
        '-t', str(image),
        'spack', 'release-jobs', '--spec-deps', str(spec),
    ]

    def add_dep(s, d):
        if s == d:
            return
        if s not in deps:
            deps[s] = set()
        deps[s].add(d)

    print(' '.join(cmd_to_run))
    proc = subprocess.Popen(cmd_to_run,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc.wait()

    out = proc.stdout.read()
    if out:
        m1 = IGNORE_SURROUND_REGEX.search(out)
        specs_and_deps = m1.group(1).strip()
        if specs_and_deps:
            # print('\n')
            # print(specs_and_deps)
            # print('\n')
            spec_label_tuples = SPEC_LINE_REGEX.findall(specs_and_deps)

            for label, spec_str in spec_label_tuples:
                spec_labels[label.strip()] = {
                    'spec': Spec(spec_str.strip()),
                    'rootSpec': spec,
                }

            dep_tuples = DEP_LINE_REGEX.findall(specs_and_deps)

            for s, d in dep_tuples:
                # print('{0} ---->>>> {1}'.format(s, d))
                add_dep(s.strip(), d.strip())

        # print('\n')
        # print('These are the spec labels I got:')
        # for spec_label in spec_labels:
        #     print('label: {0}, spec: {1}'.format(spec_label, spec_labels[spec_label]))

        # print('\n')
        # print('These are the deps I got:')
        # for dep in deps:
        #     for d in deps[dep]:
        #         print('{0} -> {1}'.format(dep, d))

    errout = proc.stderr.read()
    if errout:
        print('stderr contained:')
        print(errout)


def containerized_stage_spec_jobs(spec_set, containers):
    def remove_satisfied_deps(deps, satisfied_list):
        new_deps = {}

        for key, value in iteritems(deps):
            new_value = set([v for v in value if v not in satisfied_list])
            if new_value:
                new_deps[key] = new_value

        return new_deps

    deps = {}
    spec_labels = {}

    for spec in spec_set:
        for osname in containers:
            container_info = containers[osname]
            if 'compilers' in container_info:
                foundOne = False
                for item in container_info['compilers']:
                    if spec.compiler.satisfies(item['name']):
                        get_deps_using_container(spec, container_info, deps, spec_labels)
                        foundOne = True
                if not foundOne:
                    print('no compiler in {0} satisfied {1}'.format(osname, spec.compiler))

    dependencies = deps
    unstaged = set(spec_labels.keys())
    stages = []

    while deps:
        depends_on = set(deps.keys())
        next_stage = unstaged.difference(depends_on)
        stages.append(next_stage)
        unstaged.difference_update(next_stage)
        deps = remove_satisfied_deps(deps, next_stage)

    if unstaged:
        stages.append(unstaged.copy())

    return spec_labels, dependencies, stages


def stage_spec_jobs(spec_set):
    deptype = all_deptypes
    spec_labels = {}
    deps = {}

    def key_label(s):
        return s.dag_hash(), "%s/%s" % (s.name, s.dag_hash(7))

    def add_dep(s, d):
        if s == d:
            return
        if s not in deps:
            deps[s] = set()
        deps[s].add(d)

    def remove_satisfied_deps(deps, satisfied_list):
        new_deps = {}

        for key, value in iteritems(deps):
            new_value = set([v for v in value if v not in satisfied_list])
            if new_value:
                new_deps[key] = new_value

        return new_deps

    for spec in spec_set:
        spec.concretize()

        rkey, rlabel = key_label(spec)

        for s in spec.traverse(deptype=deptype):
            if not s.concrete:
                s.concretize()
            skey, slabel = key_label(s)
            spec_labels[slabel] = {
                'spec': s,
                'rootSpec': spec,
            }
            add_dep(rlabel, slabel)

            for d in s.dependencies(deptype=deptype):
                dkey, dlabel = key_label(d)
                add_dep(slabel, dlabel)

    dependencies = deps
    unstaged = set(spec_labels.keys())
    stages = []

    while deps:
        depends_on = set(deps.keys())
        next_stage = unstaged.difference(depends_on)
        stages.append(next_stage)
        unstaged.difference_update(next_stage)
        deps = remove_satisfied_deps(deps, next_stage)

    if unstaged:
        stages.append(unstaged.copy())

    return spec_labels, dependencies, stages


def print_staging_summary(spec_labels, dependencies, stages):
    print('Staging summary:')
    stageIndex = 0
    for stage in stages:
        print('  stage {0} ({1} jobs):'.format(stageIndex, len(stage)))

        for job in sorted(stage):
            print('    {0} -> {1}'.format(job, spec_labels[job]['spec']))

        stageIndex += 1


def dump_spec_deps(spec):
    deptype = all_deptypes
    spec_labels = {}
    deps = {}

    def key_label(s):
        return s.dag_hash(), "%s/%s" % (s.name, s.dag_hash(7))

    def add_dep(s, d):
        if s == d:
            return
        if s not in deps:
            deps[s] = set()
        deps[s].add(d)

    spec.concretize()

    rkey, rlabel = key_label(spec)

    for s in spec.traverse(deptype=deptype):
        if not s.concrete:
            s.concretize()
        skey, slabel = key_label(s)
        spec_labels[slabel] = s
        add_dep(rlabel, slabel)

        for d in s.dependencies(deptype=deptype):
            dkey, dlabel = key_label(d)
            add_dep(slabel, dlabel)

    for label in spec_labels:
        s = spec_labels[label]
        print('label: {0}, spec: {1}'.format(label, get_spec_string(s)))

    for dep_key in deps:
        for depends in deps[dep_key]:
            print('{0} -> {1}'.format(dep_key, depends))


def release_jobs(parser, args):
    share_path = os.path.join('.', 'share', 'spack', 'docker')
    os_container_mapping_path = os.path.join(
        share_path, 'os-container-mapping.yaml')

    with open(os_container_mapping_path, 'r') as fin:
        os_container_mapping = syaml.load(fin)

    validate(os_container_mapping, schema)

    containers = os_container_mapping['containers']

    if args.spec_deps:
        # look at the compiler listed on the spec and try to find a
        # container info which claims it supports that compiler
        s = Spec(args.spec_deps)
        dump_spec_deps(s)
        # for osname in containers:
        #     container_info = containers[osname]
        #     if 'compilers' in container_info:
        #         for item in container_info['compilers']:
        #             if s.compiler.satisfies(item['name']):
        #                 generate_container_deps(s, container_info)

        return

    release_specs_path = args.spec_set
    if not release_specs_path:
        raise SpackError('Must provide path to release spec-set')

    release_spec_set = CombinatorialSpecSet.from_file(release_specs_path)

    mirror_url = args.mirror_url

    if not mirror_url:
        raise SpackError('Must provide url of target binary mirror')

    cdash_url = args.cdash_url

    # spec_labels, dependencies, stages = stage_spec_jobs(release_spec_set)
    spec_labels, dependencies, stages = containerized_stage_spec_jobs(
        release_spec_set, containers)

    if args.print_summary:
        print_staging_summary(spec_labels, dependencies, stages)

    output_object = {}
    job_count = 0

    stage_names = ['stage-{0}'.format(i) for i in range(len(stages))]
    stage = 0

    for stage_jobs in stages:
        stage_name = stage_names[stage]

        for spec_label in stage_jobs:
            release_spec = spec_labels[spec_label]['spec']
            root_spec = spec_labels[spec_label]['rootSpec']

            pkg_compiler = release_spec.compiler
            pkg_hash = release_spec.dag_hash()

            for osname in containers:
                job_name = get_job_name(release_spec, osname)
                container_info = containers[osname]
                build_image = container_info['image']


                job_scripts = ['./rebuild-package.sh']

                if 'setup_script' in container_info:
                    job_scripts.insert(
                        0, container_info['setup_script'] % pkg_compiler)

                job_dependencies = []
                job_deps_env = []
                if spec_label in dependencies:
                    job_dependencies = (
                        [get_job_name(spec_labels[dep_label]['spec'], osname)
                            for dep_label in dependencies[spec_label]])

                job_object = {
                    'stage': stage_name,
                    'variables': {
                        'MIRROR_URL': mirror_url,
                        'CDASH_BASE_URL': cdash_url,
                        'HASH': pkg_hash,
                        'DEPENDENCIES': ';'.join(job_dependencies),
                        'ROOT_SPEC': str(root_spec),
                    },
                    'script': job_scripts,
                    'image': build_image,
                    'artifacts': {
                        'paths': [
                            'local_mirror/build_cache'
                        ],
                    },
                    'dependencies': job_dependencies,
                }

                # If we see 'compilers' in the container iformation, it's a
                # filter for the compilers this container can handle, else we
                # assume it can handle any compiler
                if 'compilers' in container_info:
                    do_job = False
                    for item in container_info['compilers']:
                        if pkg_compiler.satisfies(item['name']):
                            do_job = True
                            if 'path' in item:
                                job_vars = job_object['variables']
                                job_vars['SPACK_FIND_COMPILER_PATHS'] = ';'.join(
                                    item['path'])
                else:
                    do_job = True

                if args.shared_runner_tag:
                    job_object['tags'] = [args.shared_runner_tag]

                if args.signing_key:
                    job_object['variables']['SIGN_KEY_HASH'] = args.signing_key

                if do_job:
                    output_object[job_name] = job_object
                    job_count += 1

        stage += 1

    tty.msg('{0} build jobs generated in {1} stages'.format(
        job_count, len(stages)))

    final_stage = 'stage-rebuild-index'

    final_job = {
        'stage': final_stage,
        'variables': {
            'MIRROR_URL': mirror_url,
        },
        'image': build_image,
        'script': './rebuild-index.sh',
    }

    if args.shared_runner_tag:
        final_job['tags'] = [args.shared_runner_tag]

    output_object['rebuild-index'] = final_job
    stage_names.append(final_stage)
    output_object['stages'] = stage_names

    with open(args.output_file, 'w') as outf:
        outf.write(syaml.dump(output_object))
