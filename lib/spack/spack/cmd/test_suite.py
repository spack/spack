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

description = "Installs packages, provides cdash output."


def setup_parser(subparser):
    subparser.add_argument(
        '-c', '--complete', action='store_true', dest='complete',
        help='Simple is build only, complete is configure, build and test.')
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
    except PackageStillNeededError as e:
        return spec, "PackageStillNeededError"
    return spec, ""


def install_spec(spec, cdash):
    failure = False
    try:
        spec.concretize()
        tty.msg("installing... " + str(spec))
        parser = argparse.ArgumentParser()
        install.setup_parser(parser)
        # use cdash-complete if you want configure, build and test output.
        args = parser.parse_args([cdash])
        args.command = "install"
        args.no_checksum = True
        args.package = str(spec).split()
        install.install(parser, args)
    except OSError as err:
        raise   
    except Exception as ex:
        template = "An exception type: {0} occured in install"
        message = template.format(type(ex).__name__, ex.args)
        tty.msg(message)
        failure = True
        pass
    return spec, failure


def test_suite(parser, args):
    """Compiles a list of tests from a yaml file. 
    Runs Spec and concretize then produces cdash format."""
    if not args.yamlFile:
        tty.die("spack testsuite requires a yaml file.")
    if args.complete:
        # cdash-complete for configure, build and test output.
        args.log_format = 'cdash-complete' 
        cdash = '--log-format=cdash-complete'
    else:
        args.log_format = 'cdash-simple' 
        cdash = '--log-format=cdash-simple'
    
    cdash_root = "/var/spack/cdash/"
    data = ""
    cdash_path = spack.prefix + cdash_root
    sets = CombinatorialSpecSet(args.yamlFile)
    tests, dashboards = sets.readinFiles()
    # setting up tests for contretizing
    for spec in tests:
        tty.msg(spec)
        if len(spack.store.db.query(spec)) != 0:
            tty.msg(spack.store.db.query(spec))
        # uninstall all packages before installing. 
        # This will reduce the number of skipped package installs.
        if (len(spack.store.db.query(spec)) > 0):
            spec,exception = uninstall_spec(spec)
            if exception is "PackageStillNeededError":
                continue
        try:
            spec, failure = install_spec(spec,cdash)
        except Exception as e:
            tty.die(e)
            sys.exit(0)
        if not failure:
            tty.msg("Failure did not occur, uninstalling " + str(spec))
            spec, exception = uninstall_spec(spec)
    if len(dashboards) != 0:
        for dashboard in dashboards:
        # allows for multiple dashboards
            files = [name for name in glob.glob(os.path.join(path,'*.*')) if os.path.isfile(os.path.join(path,name))]
            for file in files:
                    if "dstore" not in file: 
                    #a void file found in OSX
                            with open(file) as fh:
                                    mydata = fh.read() 
                                    # using a put request to send xml files to cdash.
                                    response = requests.put(dashboard,
                                            data=mydata,
                                            headers={'content-type':'text/plain'},
                                            params={'file': cdash_path + file}
                                            )
                                    tty.msg(file)
                                    tty.msg(response.status_code)


class CombinatorialSpecSet:

    def __init__(self, files):
        self.yamlFiles = files

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

    def readinFiles(self):
        compilers = []
        packages = []
        tests = []
        dashboards = []
        compiler_version = []
        schema = spack.schema.test.schema
        for filename in self.yamlFiles: 
        # read yaml files which contains description of tests
            package_version = []
            tmp_compiler_ist = []
            try:
                tty.debug("Reading config file %s" % filename)
                with open(filename) as f:
                    data = _mark_overrides(syaml.load(f))
                if data:
                    validate_section(data, schema)
                    packages= data['test-suite']['packages'] 
                    compilers = data['test-suite']['compilers']
                    for compiler in compilers:
                            versions = compilers[compiler]['versions']
                            [tmp_compiler_ist.append(Spec(spec)) for spec in self.combinatorial(compiler,versions)]
                    for compiler in tmp_compiler_ist:
                        if any(compiler.satisfies(str(cs)) for cs in spack.compilers.all_compiler_specs()): 
                            compiler_version.append(compiler)
                    if 'include' in data['test-suite']:
                        included_tests = data['test-suite']['include']
                        for package in packages:
                            if package in included_tests:
                                versions = packages[package]['versions']
                                [package_version.append(Spec(spec)) for spec in self.combinatorial(package,versions)]
                    else:
                        for package in packages:
                            versions = packages[package]['versions']
                            [package_version.append(Spec(spec)) for spec in self.combinatorial(package,versions)]
                    [tests.append(Spec(spec)) for spec in self.combinatorial_compiler(package_version,compiler_version)]
                    if 'exclude' in data['test-suite']:
                        remove_tests = []
                        excluded_tests = data['test-suite']['exclude']
                        for spec in tests:
                            for excluded_test in excluded_tests:
                                if bool(spec.satisfies(excluded_test)):
                                    remove_tests.append(spec)
                        for test in remove_tests:
                            tests.remove(test)
                    if 'dashboard' in data['test-suite']:
                        dashboards.append(data['test-suite']['dashboard'])
            except MarkedYAMLError as e:
                raise ConfigFileError(
                    "Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))
            except IOError as e:
                raise ConfigFileError(
                    "Error reading file %s: %s" % (filename, str(e)))
        return tests, dashboards


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
