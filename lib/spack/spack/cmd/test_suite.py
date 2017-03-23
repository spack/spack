#!/usr/bin/env python

import os
import platform
import requests
import spack.package
import glob
import argparse
import llnl.util.tty as tty
from spack.spec import Spec
import spack.cmd.install as install    
import spack.cmd.uninstall as uninstall
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
import time
import traceback
concreteTests = []

description = "Compiles a list of tests from a yaml file. Runs Spec and concretize then produces cdash format."

def setup_parser(subparser):
    subparser.add_argument(
        '-c', '--complete', action='store_true', dest='complete',
        help='using this option switches from simple cdash output to compelet: simple is only build, complete is configure, build and test xml output.')
    subparser.add_argument(
        'yamlFile', nargs=argparse.REMAINDER,
        help="yaml file that contains a list of tests, example yaml file can be found in /lib/spack/docs/tutorial/examples/test.yaml")

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

def uninstallSpec(spec):
    try:
        spec.concretize()
        tty.msg("uninstalling... " + str(spec))
        pkg = spack.repo.get(spec)
        pkg.do_uninstall()
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r} uninstall"
        message = template.format(type(ex).__name__, ex.args)
        tty.msg(message)
        pass
    except PackageStillNeededError as e:
        return spec, "PackageStillNeededError"
    return spec, ""

def installSpec(spec,cdash):
    failure = False
    try:
        spec.concretize()
        tty.msg("installing... " + str(spec))
        parser = argparse.ArgumentParser()
        install.setup_parser(parser)
        args = parser.parse_args([cdash]) #use cdash-complete if you want configure, build and test output.
        args.command = "install"
        args.no_checksum = True
        args.package.append(spec)
        install.install(parser, args)
    except OSError as err:
        raise   
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r} install"
        message = template.format(type(ex).__name__, ex.args)
        tty.msg(message)
        failure = True
        pass
    return spec,failure

class CombinatorialSpecSet:

    def __init__(self,files):
        self.yamlFiles = files

    def combinatorial(self,items,versions):
         for item in items:
             for version in versions:
                spec = Spec(item)
                if spec.constrain("@" +str(version)):
                    yield spec

    def combinatorialCompiler(self,packages,compilers):
        for package in packages:
            for compiler in compilers:
                spec = Spec(package)
                if spec.constrain("%"+str(compiler)):
                    yield spec


    def readinFiles(self):
        compilers = []
        packages = []
        tests = []
        dashboards = []
        compilerVersion = []
        schema = spack.schema.test.schema
        for filename in self.yamlFiles: #read yaml files which contains description of tests
            packageVersion = []
            tmpCompilerList = []
            try:
                tty.debug("Reading config file %s" % filename)
                with open(filename) as f:
                    data = _mark_overrides(syaml.load(f))
                if data:
                    validate_section(data, schema)
                    packages= data['packages'] # list all packages available.
                    compilers = data['compilers']
                    for compiler in compilers:
                        for comp in compiler:
                            versions = compiler[comp][0]['versions']
                            [tmpCompilerList.append(Spec(spec)) for spec in self.combinatorial(compiler,versions)]
                    for compiler in tmpCompilerList:
                        print type(compiler)
                        if any(compiler.satisfies(str(cs)) for cs in spack.compilers.all_compiler_specs()): 
                            compilerVersion.append(compiler)
                    #print compilerVersion
                    if 'include' in data:
                        includedTests = data['include']
                        for package in packages:
                            for pkg in package:
                                if pkg in includedTests:
                                    versions = package[pkg][0]['versions']
                                    [packageVersion.append(Spec(spec)) for spec in self.combinatorial(package,versions)]
                    else:
                        for package in packages:
                            for pkg in package:
                                versions = package[pkg][0]['versions']
                                [packageVersion.append(Spec(spec)) for spec in self.combinatorial(package,versions)]
                    if 'exclude' in data:
                        removeTests = []
                        excludedTests = data['exclude']
                        for spec in tests:
                            for excludedTest in excludedTests:
                        #for exclusion in exclusions:
                                if bool(spec.satisfies(excludedTest)):
                                    removeTests.append(spec)
                        for test in removeTests:
                            tests.remove(test)
                    if 'dashboard' in data:
                        dashboards.append(data['dashboard'])
                [tests.append(Spec(spec)) for spec in self.combinatorialCompiler(packageVersion,compilerVersion)]
            except MarkedYAMLError as e:
                raise ConfigFileError(
                    "Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))
            except IOError as e:
                raise ConfigFileError(
                    "Error reading configuration file %s: %s" % (filename, str(e)))
        return tests, dashboards


def test_suite(parser, args):
    """Compiles a list of tests from a yaml file. Runs Spec and concretize then produces cdash format."""
    if not args.yamlFile:
        tty.die("spack testsuite requires a yaml file as argument.")
    if args.complete:
        args.log_format='cdash-complete' #use cdash-complete if you want configure, build and test output.
        cdash = '--log-format=cdash-complete'
    else:
        args.log_format='cdash-simple' #use cdash-complete if you want configure, build and test output.
        cdash = '--log-format=cdash-simple'
    
    cdash_root = "/var/spack/cdash/"
    data = ""
    cdashPath = spack.prefix+cdash_root
    #designed to use a single file and modify the enabled tests, thus requiring a single file modification.
    sets = CombinatorialSpecSet(args.yamlFile)
    tests,dashboards = sets.readinFiles()
    #setting up tests for contretizing
    for spec in tests:
        tty.msg(spec)
        if len(spack.store.db.query(spec)) != 0:
            tty.msg(spack.store.db.query(spec))
        #uninstall all packages before installing. This will reduce the number of skipped package installs.

        if (len(spack.store.db.query(spec)) > 0):
            spec,exception = uninstallSpec(spec)
            if exception is "PackageStillNeededError":
                continue
        spec,failure = installSpec(spec,cdash)
        if not failure:
            tty.msg("Failure did not occur, uninstalling " + str(spec))
            spec,exception = uninstallSpec(spec)
    #Path contains xml files produced during the test run.

    if len(dashboards) != 0:
        for dashboard in dashboards:#allows for multiple dashboards
            files = [name for name in glob.glob(os.path.join(path,'*.*')) if os.path.isfile(os.path.join(path,name))]
            for file in files:
                    if "dstore" not in file: #avoid file found in OSX
                            with open(file) as fh:
                                    mydata = fh.read() #using a put request to send xml files to cdash.
                                    response = requests.put(dashboard,
                                            data=mydata,
                                            headers={'content-type':'text/plain'},
                                            params={'file': cdashPath+file}
                                            )
                                    tty.msg(file)
                                    tty.msg(response.status_code)

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