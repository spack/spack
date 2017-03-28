##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
import requests
import spack.package
import glob
import argparse
import llnl.util.tty as tty
from spack.spec import Spec
import spack.cmd.install as install
import spack.util.spack_yaml as syaml
import spack.cmd.compiler
import spack.compilers
import spack
from yaml.error import MarkedYAMLError
import jsonschema
from jsonschema import Draft4Validator, validators
from spack.error import SpackError
import re
import sys
import datetime
import errno

description = "Installs packages, provides cdash output."


def setup_parser(subparser):
    subparser.add_argument(
        '--log-format',
        default=None,
        choices=['cdash', 'cdash-simple'],
        help="Format to be used for log files."
    )
    subparser.add_argument(
        '-s', '--site', action='store', dest='site',
        help='Location where testing occurred.')
    subparser.add_argument(
        '-d', '--cdash', action='store', dest='cdash',
        help='URL to cdash.')
    subparser.add_argument(
        '-p', '--project', action='store', dest='project',
        help='project name on cdash')
    subparser.add_argument(
        'yamlFile', nargs=argparse.REMAINDER,
        help="Yaml test descriptions. Example found in spack docs.")


def _mark_overrides(data):
    if isinstance(data, list):
        return [_mark_overrides(elt) for elt in data]

    elif isinstance(data, dict):
        marked = {}
        for key, val in data.iteritems():
            if isinstance(key, basestring) and key.endswith(':'):
                key = syaml.syaml_str(key[:-1])
                key.override = True
            marked[key] = _mark_overrides(val)
        return marked

    else:
        return data


def extend_with_default(validator_class):
    """Add support for the 'default' attr for properties and patternProperties.

       jsonschema does not handle this out of the box -- it only
       validates.  This allows us to set default values for configs
       where certain fields are `None` b/c they're deleted or
       commented out.

    """
    validate_properties = validator_class.VALIDATORS["properties"]
    validate_pattern_properties = validator_class.VALIDATORS[
        "patternProperties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.iteritems():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])
        for err in validate_properties(
                validator, properties, instance, schema):
            yield err

    def set_pp_defaults(validator, properties, instance, schema):
        for property, subschema in properties.iteritems():
            if "default" in subschema:
                if isinstance(instance, dict):
                    for key, val in instance.iteritems():
                        if re.match(property, key) and val is None:
                            instance[key] = subschema["default"]

        for err in validate_pattern_properties(
                validator, properties, instance, schema):
            yield err

    return validators.extend(validator_class, {
        "properties": set_defaults,
        "patternProperties": set_pp_defaults
    })


DefaultSettingValidator = extend_with_default(Draft4Validator)


def validate_section(data, schema):
    """Validate data read in from a Spack YAML file.

    This leverages the line information (start_mark, end_mark) stored
    on Spack YAML structures.

    """
    try:
        DefaultSettingValidator(schema).validate(data)
    except jsonschema.ValidationError as e:
        raise ConfigFormatError(e, data)


def uninstall_spec(spec):
    try:
        spec.concretize()
        tty.msg("uninstalling... " + str(spec))
        pkg = spack.repo.get(spec)
        pkg.do_uninstall()
    except Exception as ex:
        template = "Exception type: {0} occured in uninstall"
        message = template.format(type(ex).__name__, ex.args)
        tty.msg(message)
        pass
    except PackageStillNeededError as err:
        tty.msg(err)
        return spec, "PackageStillNeededError"
    return spec, ""


def install_spec(spec, cdash, site):
    failure = False
    try:
        spec.concretize()
        tty.msg("installing... " + str(spec))
        parser = argparse.ArgumentParser()
        install.setup_parser(parser)
        # use cdash-complete if you want configure, build and test output.
        args = parser.parse_args([cdash, site])
        args.command = "install"
        args.no_checksum = True
        args.package = str(spec).split()
        install.install(parser, args)
    except OSError as err:
        tty.msg(err)
        raise
    except Exception as ex:
        template = "An exception type: {0} occured in install"
        message = template.format(type(ex).__name__, ex.args)
        tty.msg(message)
        failure = True
        pass
    return spec, failure


def create_path():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    path = os.getcwd() + "/spack-test-" + str(timestamp) + "/"
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    return path


def test_suite(parser, args):
    spackio_url = "https://spack.io/cdash/submit.php?project="
    submit = "/submit.php?project="
    url = []
    project = ""
    """Compiles a list of tests from a yaml file.
    Runs Spec and concretize then produces cdash format."""
    if not args.yamlFile:
        tty.die("spack testsuite requires a yaml file.")
    if not args.log_format:
        tty.die("spack testsuite requires a log format, cdash, cdash-simple")
    cdash = '--log-format=' + str(args.log_format)
    path = create_path()
    if args.site:
        site = "--site=" + args.site
    else:
        import socket
        site = "--site=" + socket.gethostname()
    for file in args.yamlFile:
        sets = CombinatorialSpecSet(file)
        test_contents = sets.read_in_file()
        if not test_contents['tests']:
            tty.msg("No tests found, continuing.")
            continue
        # setting up tests for contretizing
        for spec in test_contents['tests']:
            tty.msg(spec)
            if len(spack.store.db.query(spec)) != 0:
                tty.msg(spack.store.db.query(spec))
            # uninstall all packages before installing.
            # This will reduce the number of skipped package installs.
            if (len(spack.store.db.query(spec)) > 0):
                spec, exception = uninstall_spec(spec)
                if exception is "PackageStillNeededError":
                    continue
            try:
                spec, failure = install_spec(spec, cdash, site)
            except Exception as e:
                tty.die(e)
                sys.exit(0)
            if not failure:
                tty.msg("Failure did not occur, uninstalling " + str(spec))
                spec, exception = uninstall_spec(spec)
        if 'project' in test_contents:
            project = test_contents['project']
        if args.cdash and args.project:
            url.append(args.cdash + submit + args.project)
        elif args.cdash and project:
            url.append(args.cdash + submit + project)
        elif args.project:
            if test_contents['cdash']:
                for cdash in test_contents['cdash']:
                    url.append(cdash + submit + args.project)
            else:
                url.append(spackio_url + args.project)
        elif 'cdash' in test_contents:
                if test_contents['cdash'] and project:
                    if len(test_contents['cdash']) > 1:
                        for cdash in test_contents['cdash']:
                            url.append(cdash + submit + str(project))
                    else:
                        url.append(test_contents['cdash'][0] +
                                   submit + project)
                elif project:
                    url.append(spackio_url + project)
        for dashboard in url:
            tty.msg("URL: " + str(dashboard))
            # allows for multiple dashboards
            # correct in future to be dynamic
            files = [name for name in glob.glob(os.path.join(path, '*.*'))
                     if os.path.isfile(os.path.join(path, name))]
            for file in files:
                if "dstore" not in file:
                        # void file found in OSX
                    with open(file) as fh:
                        mydata = fh.read()
                        # PUT request to send xml files to cdash.
                        response = requests.put(
                            dashboard,
                            data=mydata,
                            headers={
                                'content-type': 'text/plain'},
                            params={
                                'file': file}
                        )
                        tty.msg(file)
                        tty.msg(response.status_code)


class CombinatorialSpecSet:

    def __init__(self, file):
        self.yaml_file = file

    def combinatorial(self, item, versions):
        for version in versions:
            spec = Spec(item)
            if spec.constrain("@" + str(version)):
                yield spec

    def combinatorial_compiler(self, packages, compilers):
        for package in packages:
            for compiler in compilers:
                spec = Spec(package)
                if spec.constrain("%" + str(compiler)):
                    yield spec

    def read_in_file(self):
        compilers = []
        packages = []
        tests = []
        compiler_version = []
        schema = spack.schema.test.schema
        package_version = []
        tmp_compiler_ist = []
        test_contents = {}
        try:
            # read yaml file which contains description of tests
            tty.debug("Reading config file %s" % self.yaml_file)
            with open(self.yaml_file) as f:
                data = _mark_overrides(syaml.load(f))
            if data:
                validate_section(data, schema)
                packages = data['test-suite']['packages']
                compilers = data['test-suite']['compilers']
                for compiler in compilers:
                    versions = compilers[compiler]['versions']
                    [tmp_compiler_ist.append(Spec(spec))
                        for spec in self.combinatorial(compiler, versions)]
                for compiler in tmp_compiler_ist:
                    if any(compiler.satisfies(str(cs))
                           for cs in spack.compilers.all_compiler_specs()):
                        compiler_version.append(compiler)
                    else:
                        tty.warn("Spack could not find " + str(compiler))
                if 'include' in data['test-suite']:
                    included_tests = data['test-suite']['include']
                    for package in packages:
                        if package in included_tests:
                            versions = packages[package]['versions']
                            [package_version.append(Spec(spec))
                                for spec in self.combinatorial(
                                    package, versions)]
                else:
                    for package in packages:
                        versions = packages[package]['versions']
                        [package_version.append(Spec(spec))
                            for spec in self.combinatorial(
                                package, versions)]
                [tests.append(Spec(spec))
                 for spec in self.combinatorial_compiler(
                    package_version, compiler_version)]
                if 'exclude' in data['test-suite']:
                    remove_tests = []
                    excluded_tests = data['test-suite']['exclude']
                    for spec in tests:
                        for excluded_test in excluded_tests:
                            if bool(spec.satisfies(excluded_test)):
                                remove_tests.append(spec)
                    for test in remove_tests:
                        tests.remove(test)
                test_contents['tests'] = tests
                if 'cdash' in data['test-suite']:
                    test_contents['cdash'] = data['test-suite']['cdash']
                if 'project' in data['test-suite']:
                    test_contents['project'] = data['test-suite']['project']
            return test_contents
        except MarkedYAMLError as e:
            raise ConfigFileError(
                "Error parsing yaml%s: %s" %
                (str(e.context_mark), e.problem))
        except IOError as e:
            raise ConfigFileError(
                "Error reading file %s: %s" %
                (filename, str(e)))


class ConfigError(SpackError):
    pass


class ConfigFileError(ConfigError):
    pass


class PackageStillNeededError(SpackError):
    """Raised when package is still needed by another on uninstall."""
    pass


class ConfigFormatError(ConfigError):
    """Raised when a configuration format does not match its schema."""

    def __init__(self, validation_error, data):
        # Try to get line number from erroneous instance and its parent
        instance_mark = getattr(validation_error.instance, '_start_mark', None)
        parent_mark = getattr(validation_error.parent, '_start_mark', None)
        path = [str(s) for s in getattr(validation_error, 'path', None)]

        # Try really hard to get the parent (which sometimes is not
        # set) This digs it out of the validated structure if it's not
        # on the validation_error.
        if path and not parent_mark:
            parent_path = list(path)[:-1]
            parent = get_path(parent_path, data)
            if path[-1] in parent:
                if isinstance(parent, dict):
                    keylist = parent.keys()
                elif isinstance(parent, list):
                    keylist = parent
                idx = keylist.index(path[-1])
                parent_mark = getattr(keylist[idx], '_start_mark', None)

        if instance_mark:
            location = '%s:%d' % (instance_mark.name, instance_mark.line + 1)
        elif parent_mark:
            location = '%s:%d' % (parent_mark.name, parent_mark.line + 1)
        elif path:
            location = 'At ' + ':'.join(path)
        else:
            location = '<unknown line>'

        message = '%s: %s' % (location, validation_error.message)
        super(ConfigError, self).__init__(message)
