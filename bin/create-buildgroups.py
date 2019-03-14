#!/usr/bin/env python

import argparse
import os
import re
import requests
import sys

from ruamel.yaml import YAML


yaml = YAML(typ='safe')
job_name_regex = re.compile('([^\\s]+)\\s+([^\\s]+)\\s+([^\\s]+)\\s+([^\\s]+)\\s+([^\\s]+)')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CDash BuildGroup Creator")
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument("-c", "--credentials",
        help="path to file containing a CDash authentication token",
        default=None, required=True)
    requiredNamed.add_argument("-f", "--buildfile",
        help="Text file containing a list of expected build names (one per line)",
        required=True)
    requiredNamed.add_argument("-p", "--projectid",
        help="The Id of the project in CDash that you'd like to modify",
        required=True)
    requiredNamed.add_argument("-s", "--siteid",
        help="The Id of the site in CDash that will be submitting the builds",
        required=True)
    requiredNamed.add_argument("-u", "--cdash-url",
        help="CDash base URL (index.php removed)",
        required=True)
    args = parser.parse_args()

    print('Creating buildgroups:')
    print('  credentials {0}'.format('provided' if args.credentials else 'NOT provided'))
    print('  buildfile: {0}'.format(args.buildfile))
    print('  projectid: {0}'.format(args.projectid))
    print('  siteid: {0}'.format(args.siteid))
    print('  cdash-url: {0}'.format(args.cdash_url))


    with open(args.buildfile, "r") as build_file:
        # Create the BuildGroup and a corresponding "Latest" BuildGroup.
        auth_token = args.credentials
        headers = {"Authorization": "Bearer {0}".format(auth_token)}
        url = "{0}/api/v1/buildgroup.php".format(args.cdash_url)

        group_id_map = {}

        def create_buildgroup(args, headers, url, group_name, group_type):
            payload = {
                "newbuildgroup": group_name,
                "projectid": args.projectid,
                "type": group_type
            }
            r = requests.post(url, json=payload, headers=headers)
            if not r.ok:
                print("Problem creating '{0}' group: {1} / {2}\n".format(group_name, r.status_code, r.text))
                sys.exit(1)
            return r.json()['id']

        def get_buildgroup(group_name):
            if group_name not in group_id_map:
                group_id_map[group_name] = {
                    'daily': create_buildgroup(args, headers, url, group_name, "Daily"),
                    'latest': create_buildgroup(args, headers, url, "Latest {0}".format(group_name), "Latest"),
                }
            groupids = group_id_map[group_name]
            return groupids['daily'], groupids['latest']

        # Populate the 'Latest' BuildGroup with our list of expected builds.
        ci_jobs = yaml.load(build_file.read())

        for job_name, job_entry in ci_jobs.items():
            print('    job_name: {0}'.format(job_name))
            m = job_name_regex.search(job_name)
            if m:
                pkg_name = m.group(1)
                pkg_version = m.group(2)
                compiler = m.group(3)
                os_arch = m.group(4)
                release_tag = m.group(5)

                daily_groupid, latest_groupid = get_buildgroup(release_tag)
                build_name = '{0}@{1}%{2} arch={3} ({4})'.format(
                pkg_name, pkg_version, compiler, os_arch, release_tag)

                payload = {
                    "match": build_name,
                    "projectid": args.projectid,
                    "buildgroup": {"id": daily_groupid},
                    "dynamic": {"id": latest_groupid},
                    "site": {"id": args.siteid},
                }
                print('      Sending payload: {0}'.format(payload))
                r = requests.post(url, json=payload, headers=headers)
                if not r.ok:
                    print("Problem creating dynamic row for '{0}': {1} / {2}\n".format(build_name, r.status_code, r.text))
                    sys.exit(1)
        print("Success")
