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
import sys
import yaml

import llnl.util.tty as tty
from spack.error import SpackError
from spack.util.spec_set import CombinatorialSpecSet

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
    share_path = os.path.join('.', 'share', 'spack')
    common_scripts_dir = os.path.join(share_path, 'docker', 'build', 'common')

    os_container_mapping = {
        'linux-ubuntu16.04-x86_64': {
            'image': 'ubuntu:16.04',
            'setup_script': os.path.join(common_scripts_dir,
                'install-tools-ubuntu-16.04-%s.sh')
        }
    }

    release_specs_path = args.spec_set
    if not release_specs_path:
        raise SpackError('Must provide path to release spec-set')

    release_spec_set = None

    with open(release_specs_path, 'r') as fin:
        release_specs_contents = fin.read()
        release_specs_yaml = yaml.load(release_specs_contents)

        # For now, turn off ignoring invalid specs, as it blocks iterating
        # the specs if the specified compilers can't be found.
        release_spec_set = CombinatorialSpecSet(release_specs_yaml,
                                                ignore_invalid=False)

    if not release_spec_set:
        tty.msg('No configured release specs, exiting.')
        return

    mirror_url = args.mirror_url
    single_stage = 'stage01'

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
        pkg_name = release_spec.name
        pkg_version = release_spec.version
        pkg_short_spec = release_spec.short_spec
        pkg_compiler = release_spec.compiler
        pkg_spec_name = release_spec.format()
        pkg_short_hash = release_spec.dag_hash()

        for osname in os_container_mapping:
            job_name = '%s / %s' % (release_spec, osname)
            container_info = os_container_mapping[osname]
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
                    'SHORT_HASH': pkg_short_hash,
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
        outf.write(yaml.dump(output_object))
