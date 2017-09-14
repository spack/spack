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
import sys
import traceback
import spack.package
import glob
import argparse
import datetime
import operator
import spack
import spack.cmd.compiler
import spack.compilers
import spack.error
import time
import shutil

import llnl.util.tty as tty
from spack.cmd.install import install
from spack.cmd.install import setup_parser as install_setup_parser
from spack.cmd.uninstall import uninstall
from spack.cmd.uninstall import setup_parser as uninstall_setup_parser
from spack.util.executable import which, ProcessError
from spack.util.web import diagnose_curl_error
from spack.util.spec_set import CombinatorialSpecSet
from spack.package import PackageStillNeededError, _hms
from spack.build_environment import InstallError
from spack.util.generate_tests import GenerateTests
from spack.database import Database
from spack.directory_layout import YamlDirectoryLayout
from contextlib import contextmanager


description = "test-installs packages and generates cdash output"
section = "developer"
level = "long"


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
        '-gt', '--generate-tests', action='store_true',
        help='generate tests')
    subparser.add_argument(
        '--gt-type', choices=['all-tests', 'days', 'xsdk'],
        default='all-tests',
        help='type of tests to generate. Default is all-tests')
    subparser.add_argument(
        '--gt-by-compiler', action='store_true',
        help='Seperate file per compiler')
    subparser.add_argument(
        '--gt-system-compilers', action='store_true',
        help='Use compilers found on system.')
    subparser.add_argument(
        '-p', '--performance', action='store_true',
        help='sorts specs for better performance')
    subparser.add_argument(
        '-t', '--time', action='store_true',
        help='Output timing for tests')
    subparser.add_argument(
        '-r', '--redundant_installs', action='store_true',
        help='Given a yaml file, output all redundant builds.')
    subparser.add_argument(
        '-u', '--uninstall_after', action='store_true',
        help='uninstall pkgs after test is successful.')
    subparser.add_argument(
        '--latest_versions', action='store_true',
        help='use latest version of package when generating test files.')
    subparser.add_argument(
        'yaml_files', nargs=argparse.REMAINDER,
        help="YAML test suite files, or a directory of them")


# used for redundant builds
dict_pkgs = {}


def update_dict(pkg):
    global dict_pkgs
    if str(pkg) in dict_pkgs.keys():
        dict_pkgs[pkg] += 1
    else:
        dict_pkgs[pkg] = 1


def find_multiples():
    pkgs = {}
    for key, value in dict_pkgs.iteritems():
        if value > 1:
            pkgs[key] = value
    sorted_redundants = sorted(
        pkgs.items(), key=operator.itemgetter(1), reverse=True)
    if not sorted_redundants:
        tty.msg("No redundant installs found.")
    else:
        for pkg in sorted_redundants:
            tty.msg(pkg[0])


def uninstall_all_specs():
    try:
        parser = argparse.ArgumentParser()
        uninstall_setup_parser(parser)
        all_pkgs = "--all"
        yes = "--yes-to-all"
        args = parser.parse_args([all_pkgs, yes])
        tty.msg("uninstalling all pkgs... ")
        uninstall(parser, args)
    except PackageStillNeededError as err:
        tty.msg(err)
        raise


def uninstall_spec(spec):
    try:
        pkg = spack.repo.get(spec)
        pkg.do_uninstall()
    except PackageStillNeededError as err:
        tty.msg(err)
        raise


def install_spec(spec, cdash, site, path, redundant=False):
    try:
        parser = argparse.ArgumentParser()
        install_setup_parser(parser)
        if redundant:
            fake = '--fake'
            redundant_arg = '--redundant'
            args = parser.parse_args([cdash, site, path, fake, redundant_arg])
        else:
            args = parser.parse_args([cdash, site, path])
        args.package = str(spec).split()
        install(parser, args)

    except OSError as err:
        traceback.print_exc(file=sys.stdout)
        tty.error(err)
        raise
    except InstallError as err:
        traceback.print_exc(file=sys.stdout)
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
        try:
            return_code = curl('--upload-file', xml_file, dashboard)
            if return_code > 0:
                tty.warn("Uploading %s to %s failed: " % (xml_file, dashboard),
                         diagnose_curl_error(return_code))
            else:
                os.remove(xml_file)
        except ProcessError:
            tty.die("Curl exited with failure.")


def get_spec_length(spec):
    return spec.tree().count('^')


def sort_list_largest_first(spec_sets, args):
    spec_dict = {}
    return_list = []
    for i, spec_set in enumerate(spec_sets):
        if args.performance:
            tty.msg("sorting tests to help with performance.")
            for spec in spec_set:
                try:
                    spec_dict[spec] = 0
                    concrete = spec.concretized()
                    spec_dict[spec] = get_spec_length(concrete)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    continue
            sorted_list = sorted(spec_dict.items(), key=operator.itemgetter(1),
                                 reverse=True)
            [return_list.append(spec[0]) for spec in sorted_list]
            tty.msg("sorting complete.... Running tests.")
            return return_list, spec_set.cdash, spec_set.project
        else:
            return spec_set, spec_set.cdash, spec_set.project


@contextmanager
def setup_test_db(tmp_db):
    """create fake install directory and a fake db into Spack."""
    tty.msg("Creating mock database for building.")
    layout = spack.store.layout
    db = spack.store.db
    # Use a fake install directory to avoid conflicts bt/w
    # installed pkgs and mock packages.
    spack.store.layout = YamlDirectoryLayout(str(tmp_db))
    spack.store.db = Database(str(tmp_db))
    yield
    shutil.rmtree(tmp_db)
    # Restore Spack's layout.
    spack.store.layout = layout
    spack.store.db = db
    tty.msg("Restoring user database.")


def test_suite(parser, args):
    """Compiles a list of tests from a yaml file.
    Runs Spec and concretize then produces cdash format."""
    # pytest.ini lives in the root of the spack repository.
    if args.time:
        start = time.time()
    if args.generate_tests:
        sep_by_cmplrs = False
        use_system_compilers = False
        latest_versions = False
        if args.gt_by_compiler:
            sep_by_cmplrs = True
        if args.gt_system_compilers:
            use_system_compilers = True
        if args.latest_versions:
            latest_versions = True
        GenerateTests(use_system_compilers, sep_by_cmplrs,
                      args.gt_type, latest_versions)
        tty.msg("test files created.")
    else:
        with setup_test_db(os.getcwd() + "test_db"):
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
                """print a warning, and stacktrace if we're
                in debug mode (spack -d)"""
                tty.warn(err)
                if spack.debug:
                    print(traceback.format_exc())

            spec_set, spec_cdash, spec_project = sort_list_largest_first(
                spec_sets, args)

            # Set cdash and project form command, then yaml file, then
            # default.
            cdash = args.cdash or spec_cdash or ['https://spack.io/cdash']
            if not isinstance(cdash, list):
                cdash = [cdash]
            project = args.project or spec_project or 'spack'

            # Send results to each dashboard.
            if not spec_project:
                urls = [
                    '{0}/submit.php?project={1}'.format(c, project)
                    for c in cdash]
            else:
                urls = spec_cdash

            # iterate over specs from each YAML file.
            for spec in spec_set:
                if args.time:
                    build_start = time.time()
                if not spec.name:
                    tty.warn(
                        "%s defines an unconcretizable spec set." % yaml_files[
                            i],
                        "Got anonymous spec: " + str(spec))
                    continue
                try:
                    concrete = spec.concretized()
                    # if we're doing a dry run, just print the concrete spec
                    if args.dry_run:
                        print(concrete.tree(
                            hashes=True, hashlen=7,
                            color=sys.stdout.isatty()))
                        continue
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    tty.warn('Concretize failed, moving on.')
                    warn(e)
                    continue

                # do the actual install
                try:
                    install_spec(spec, log_format, site,
                                 patharg, args.redundant_installs)
                    if args.uninstall_after:
                        uninstall_spec(concrete)
                except KeyboardInterrupt:
                    raise

                except Exception as e:
                    tty.warn('Install hit exception, moving on.')
                    warn(e)
                    traceback.print_exc(file=sys.stdout)
                    continue

                except PackageStillNeededError as err:
                    tty.warn('Package still needed, cant uninstall.')
                    warn(err)
                    continue

                if args.time:
                    tty.msg(str(spec.name) + "@" + str(spec.version) +
                            " Build time:  " + _hms(time.time() - build_start))
                if not args.redundant_installs:
                    for dashboard in urls:
                        send_reports(dashboard, path)

            if args.time:
                tty.msg("Total build time : " + _hms(time.time() - start))

            if args.redundant_installs:
                find_multiples()
                uninstall_all_specs()
