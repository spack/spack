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

from jsonschema import validate
from six import iteritems

from spack.dependency import all_deptypes
from spack.error import SpackError
from spack.schema.os_container_mapping import schema
from spack.util.spec_set import CombinatorialSpecSet
import spack.util.spack_yaml as syaml

description = "generate release build set as .gitlab-ci.yml"
section = "build"
level = "long"


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
            newValue = set([v for v in value if v not in satisfied_list])
            if newValue:
                new_deps[key] = newValue

        return new_deps

    for spec in spec_set:
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


def release_jobs(parser, args):
    share_path = os.path.join('.', 'share', 'spack', 'docker')
    os_container_mapping_path = os.path.join(
        share_path, 'os-container-mapping.yaml')

    with open(os_container_mapping_path, 'r') as fin:
        os_container_mapping = syaml.load(fin)

    validate(os_container_mapping, schema)

    containers = os_container_mapping['containers']

    release_specs_path = args.spec_set
    if not release_specs_path:
        raise SpackError('Must provide path to release spec-set')

    release_spec_set = CombinatorialSpecSet.from_file(release_specs_path)

    mirror_url = args.mirror_url

    if not mirror_url:
        raise SpackError('Must provide url of target binary mirror')

    spec_labels, dependencies, stages = stage_spec_jobs(release_spec_set)

    output_object = {}

    stage_names = ['stage-{0}'.format(i) for i in range(len(stages))]
    stage = 0

    def get_job_name(spec, osname):
        return '{0}'.format(spec.short_spec)
        # return '{0} / {1}'.format(spec.short_spec, osname)

    for stage_jobs in stages:
        stage_name = stage_names[stage]

        for spec_label in stage_jobs:
            release_spec = spec_labels[spec_label]

            pkg_short_spec = release_spec.short_spec
            pkg_compiler = release_spec.compiler
            pkg_spec_name = release_spec.format()
            pkg_hash = release_spec.dag_hash()

            for osname in containers:
                job_name = get_job_name(release_spec, osname)
                container_info = containers[osname]
                build_image = container_info['image']
                setup_script = container_info['setup_script'] % pkg_compiler

                job_dependencies = []
                if spec_label in dependencies:
                    job_dependencies = (
                        [get_job_name(spec_labels[dep_label], osname)
                            for dep_label in dependencies[spec_label]])

                output_object[job_name] = {
                    'stage': stage_name,
                    'variables': {
                        'SHORT_SPEC': pkg_short_spec,
                        'MIRROR_URL': mirror_url,
                        'HASH': pkg_hash,
                        'SPEC_NAME': pkg_spec_name
                    },
                    'script': [
                        setup_script,
                        './rebuild-package.sh'
                    ],
                    'image': build_image,
                    'artifacts': {
                        'paths': [
                            'buildcache'
                        ],
                    },
                    'dependencies': job_dependencies,
                    'tags': ['my-tag']
                }

        stage += 1

    output_object['stages'] = stage_names

    with open(args.output_file, 'w') as outf:
        outf.write(syaml.dump(output_object))
