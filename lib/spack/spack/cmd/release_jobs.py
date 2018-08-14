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


def release_jobs(parser, args):
    share_path = os.path.join('.', 'share', 'spack', 'docker')
    os_container_mapping_path = os.path.join(share_path, 'os-container-mapping.yaml')

    with open(os_container_mapping_path, 'r') as fin:
        os_container_mapping = syaml.load(fin)

    validate(os_container_mapping, schema)

    release_specs_path = args.spec_set
    if not release_specs_path:
        raise SpackError('Must provide path to release spec-set')

    release_spec_set = CombinatorialSpecSet.from_file(release_specs_path)

    mirror_url = args.mirror_url
    # single_stage = 'stage01'

    if not mirror_url:
        raise SpackError('Must provide url of target binary mirror')

    # output_object = {
    #     'stages': [ single_stage ]
    # }

    output_object = {}

    # job_count = 0
    # stages = []

    stage_name = 'stage-01'
    stages = [stage_name]

    for release_spec in release_spec_set:
        pkg_short_spec = release_spec.short_spec
        pkg_compiler = release_spec.compiler
        pkg_spec_name = release_spec.format()
        pkg_hash = release_spec.dag_hash()

        containers = os_container_mapping['containers']
        for osname in containers:
            job_name = '%s / %s' % (release_spec, osname)
            container_info = containers[osname]
            build_image = container_info['image']
            setup_script = container_info['setup_script'] % pkg_compiler

            # stage_name = 'stage-%d' % job_count
            # job_count += 1
            # stages.append(stage_name)

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
                'tags': ['my-tag']
            }

    output_object['stages'] = stages

    with open(args.output_file, 'w') as outf:
        outf.write(syaml.dump(output_object))
