##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import traceback
import spack.package
import glob
import argparse
import datetime

import llnl.util.tty as tty

import spack
import spack.cmd.install as install
import spack.cmd.compiler
import spack.compilers
import spack.error
from spack.util.executable import which
from spack.util.web import diagnose_curl_error
from spack.util.spec_set import CombinatorialSpecSet
from spack.package import PackageStillNeededError


description = "test installation of a suite of packages; generate cdash output"


def setup_parser(subparser):
    subparser.add_argument(
        '--log-format', choices=['cdash', 'cdash-simple'],
        default='cdash-simple', help="format to use for log files")
    subparser.add_argument(
        '--site', action='store', help='Location where testing occurred.')
    subparser.add_argument(
        '--cdash', action='store', default=None,
        help='URL of a cdash server (default spack.io/cdash)')
    subparser.add_argument(
        '--project', action='store', default=None,
        help='project name on cdash (default spack)')
    subparser.add_argument(
        '-o', '--output', metavar='dir', action='store', default=None,
        help='output directory for test data')
    subparser.add_argument(
        '--dry-run', action='store_true',
        help='only print specs that would be installed')
    subparser.add_argument(
        'yaml_files', nargs=argparse.REMAINDER,
        help="YAML test suite files, or a directory of them")


def uninstall_spec(spec):
    try:
        tty.msg("uninstalling... " + str(spec))
        pkg = spack.repo.get(spec)
        pkg.do_uninstall()
    except PackageStillNeededError as err:
        tty.msg(err)
        raise


def install_spec(spec, cdash, site, path):
    try:
        tty.msg("installing... " + str(spec))
        parser = argparse.ArgumentParser()
        install.setup_parser(parser)
        args = parser.parse_args([cdash, site, path])
        args.package = str(spec).split()
        install.install(parser, args)
    except OSError as err:
        tty.error(err)
        raise
    except InstallError as err:
        tty.error(err)
        raise


def create_output_directory(path=None):
    """Create output directory to store CDash files."""
    if path is None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(os.getcwd(), "spack-test-" + str(timestamp))

    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        tty.die("Path already exists and is not a directory: ", path)

    return path


def valid_yaml_files(candidates):
    """Validate test file locations passed on the command line."""
    valid_files = []
    for file in candidates:
        if os.path.isdir(file):
            # directory full of YAML files
            valid_files.extend(
                name for name in glob.glob(os.path.join(file, '*.yaml'))
                if os.path.isfile(os.path.join(file, name)))

        elif os.path.isfile(file):
            # user gave path to file, parse and return
            if file.endswith('.yaml'):
                valid_files.append(file)
        else:
            tty.die("Not a valid file or directory.")

    return valid_files


def send_reports(dashboard, path):
    tty.msg("Sending reports to " + str(dashboard))

    # allows for multiple dashboards
    # correct in future to be dynamic
    files = glob.glob(os.path.join(path, '*.xml'))

    # use curl to send files to CDash.
    curl = which('curl', required=True)

    # -f causes curl to fail silently and return an error code.
    # -L follows redirects.
    # -k is used when running spack -k, to skip cert checks.
    curl.add_default_arg('-fL')
    if spack.insecure:
        curl.add_default_arg('-k')

    for xml_file in files:
        if not os.path.isfile(xml_file):
            continue

        return_code = curl('--upload-file', xml_file, dashboard)
        if return_code != 0:
            tty.warn("Uploading %s to %s failed: " % (xml_file, dashboard),
                     diagnose_curl_error(return_code))


def test_suite(parser, args):
    """Compiles a list of tests from a yaml file.
    Runs Spec and concretize then produces cdash format."""
    if not args.yaml_files:
        tty.die("spack test-suite requires at least one argument")

    # Figure out which inputs are YAML files, or glob them out of a
    # directory if needed.
    yaml_files = valid_yaml_files(args.yaml_files)
    if not yaml_files:
        tty.die("no input files were valid")

    # Make spec sets out of each file.  This validates the schemas in
    # advance of building anything, so that we fail fast.
    spec_sets = []
    for yfile in yaml_files:
        with open(yfile) as f:
            spec_sets.append(CombinatorialSpecSet(f))

    log_format = '--log-format=' + str(args.log_format)

    path = create_output_directory()
    patharg = "--path=" + str(path)
    if args.site:
        site = "--site=" + args.site
    else:
        import socket
        site = "--site=" + socket.gethostname()

    def warn(err):
        """print a warning, and stacktrace if we're in debug mode (spack -d)"""
        tty.warn(err)
        if spack.debug:
            print(traceback.format_exc())

    # iterate over specs from each YAML file.
    for i, spec_set in enumerate(spec_sets):
        for spec in spec_set:
            if not spec.name:
                tty.warn(
                    "%s defines an unconcretizable spec set." % yaml_files[i],
                    "Got anonymous spec: " + str(spec))
                continue

            try:
                concrete = spec.concretized()

                # if we're doing a dry run, just print the concrete spec
                if args.dry_run:
                    print(concrete.tree(color=sys.stdout.isatty()))
                    continue

            except KeyboardInterrupt:
                raise
            except Exception as e:
                tty.warn('Concretize failed, moving on.')
                warn(e)
                continue

            # if the spec is already installed, uninstall it before
            # trying to install.
            # TODO: this is destructive; consider a separate sandbox root.
            if spack.store.db.query(spec):
                tty.msg(spack.store.db.query(spec))
                try:
                    uninstall_spec(spec)

                except PackageStillNeededError as err:
                    tty.warn('Package still needed, cant uninstall.')
                    warn(err)
                    continue   # note: this skips the install.
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    tty.warn('Unexpected error.')
                    warn(err)

            # do the actual install
            try:
                install_spec(spec, log_format, site, patharg)
                uninstall_spec(spec)

            except KeyboardInterrupt:
                raise
            except Exception as e:
                tty.warn('Install hit exception, moving on.')
                warn(e)
                continue

        # Set cdash and project form command, then yaml file, then default.
        cdash = args.cdash or spec_set.cdash or ['https://spack.io/cdash']
        if not isinstance(cdash, list):
            cdash = [cdash]
        project = args.project or spec_set.project or 'spack'

        # Send results to each dashboard.
        urls = ['{0}/submit.php?project={1}'.format(c, project) for c in cdash]
        for dashboard in urls:
            send_reports(dashboard, path)
