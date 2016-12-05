import os

import llnl.util.filesystem
from llnl.util.lang import key_ordering
import llnl.util.tty as tty
from spack.util.spack_yaml import syaml_dict
import spack.util.executable
import spack.spec


class PackageConfigEntry(object):
    """
    Class represents a package configuration entry.
    Attributes:
        package:        the entire dictionary for the package entry
        package_name:   name of the package
        external_type:  modules or paths
        specs:          specs dictionary
    Methods:
        update_specs:   add a new spec to the specs dictionary
        remove_spec:    given a spec, remove it from dictionary
        config_entry:   turns package config entry into a syaml dict
    """
    def __init__(self, package_name, package_entry):
        self.package_name = package_name
        self.package = package_entry
        self.external_type = self._find_external_type()
        self.specs = self._get_specs(self.external_type)

    def specs_section(self):
        return self.specs

    def is_spec_empty(self):
        return self.specs == {}

    def is_empty(self):
        return self.package == {}

    def update_specs(self, update_spec):
        """
        Adds specs to the specs_section of a package config
        updates the package_dict attribute
        """
        self.specs.update(update_spec)
        self.package[self.external_type] = self.specs

    def remove_spec(self, spec_to_be_removed):
        """
        Remove a spec from the specs section
        """
        filtered_specs = self._filter_specs(spec_to_be_removed)
        self.specs = filtered_specs
        self.package[self.external_type] = filtered_specs

    def _filter_specs(self, spec): 
        """Filter out specs that don't match the input spec"""
        return {k: v for k, v in self.specs_section().iteritems() if
                k != str(spec)}

    def _get_specs(self, external_type):
        return self.package.get(external_type, {})

    def _find_external_type(self):
        valid_types = ["modules", "paths"]
        for external in valid_types:
            specs_section = self._get_specs(external)
            if specs_section:
                return external
 
    def config_entry(self):
        """Turn object into config entry"""
        return {self.package_name: self.package}


class PackagesConfig(object):
    """
    Class represents the packages.yaml config file.

    Attributes:
        scope:            scope of the config file to be manipulated
    Methods:
        get_package:              returns a PackageConfigEntry object
        update_package_config:    given a package dict, updates config file
        remove_entire_entry_from_config:    remove an entire package entry
    """

    def __init__(self, scope):
        self._scope = scope
        self._packages_config = spack.config.get_config("packages", scope)

    def get_package(self, package_name):
        """
        Given a package name, return a PackageConfigEntry object.
        PackageConfigEntry represents a config entry. Can be manipulated
        """
        packages = spack.config.get_config("packages", self._scope)
        return PackageConfigEntry(package_name,
                                  self._packages_config.get(package_name, {}))

    def update_package_config(self, package_entry):
        """Update packages.yaml package entry"""
        spack.config.update_config("packages", package_entry, self._scope)
        # ordered dict so can assume first entry is package name
        package_name = package_entry.keys()[0]
        tty.msg("Added {0} external package".format(package_name))

    def remove_entire_entry_from_config(self, package_name):
        """Remove an entire package name from the config"""
        self._packages_config.pop(package_name)
        self._overwrite_package_config()
        tty.msg("Removed {0}".format(package_name))

    def all_external_packages(self):
        all_packages = []
        for package_name, entry in self._packages_config.iteritems():
            if package_name == "all":
                continue
            all_packages.append(PackageConfigEntry(package_name, entry))
        return all_packages

    def _overwrite_package_config(self):
        scope = spack.config.validate_scope(self._scope)
        scope.sections["packages"] = {'packages': self._packages_config}
        scope.write_section("packages")


def detect_version_by_prefix(path):
    """
    Return a version string if it is detected from a prefix.

    Parses through the path directory names and searches for a string.
    If a match is found, return that string.
    """

    def directory_string_represents_version(directory_name):
        """
        Returns true if directory name satisfies a version format
        """
        try:
            if "-" in directory_name:
                dir_list = directory_name.split("-")
                number_list = dir_list[1]
            else:
                number_list = directory_name.split(".")
            int(number_list[0])
            return True
        except ValueError:
            return False

    directory_names = path.split("/")
    for directory in directory_names:
        if directory_string_represents_version(directory):
            return directory
        else:
            continue


def detect_version_by_module(module_name):
    """
    Return a version string.

    Parses output of module command. If it is able to find a successful match
    return the version string.
    """
    module_command = spack.util.executable.which("modulecmd")
    if module_command:
        module_command.add_default_arg("python")
        output = module_command("avail", module_name, output=str, error=str)
        for line in output:
            if "_VERSION" in line or "_VER" in line:
                line_split = line.split()
                version = line_split[len(line_split) - 1]
                return version


def detect_version(external_location):
    """
    Return a version string from called methods.

    Calls different ways to detect a version and places them in a set.
    If the set size is equal to one then pop the string out and return the
    string.
    """

    def execute(function_to_call):
        """Helper method to call functions with or without arguments"""
        func, args = function_to_call
        if args:
            return func(args)
        else:
            return func()

    detection_strategies = [(detect_version_by_module,
                             external_location),
                            (detect_version_by_prefix,
                             external_location)]

    successful_checks = {ver for ver in map(execute, detection_strategies) 
                         if ver is not None}

    # If our checks provided us with a single version then return that.
    # Return nothing even if multiple versions were found, we only want one
    # single version and want to avoid multiple version conflicts
    if len(successful_checks) == 1:
        return successful_checks.pop()


@key_ordering
class ExternalPackage(object):
    """
    Class creates external package objects.
    Attributes:
        spec               Spec object that describes the external package
        external_location  either a path or a module describing how package
                           can be located.
        external_type      Is the type a path or a module
        buildable          Is package meant to be built by Spack?

    Properties:
        version             Returns the version of external_package
        name                Name of the package
        external_type       Either module or path
        external_location   How the package is meant to be found
        spec                Returns spec object of external package
    Methods:
        spec_section        Returns spec section of a config dict
        to_config_entry     Constructs a "config" representation of object
        create_external_package  Alternate constructor for ExternalPackage.
                                 This does do validate type and location
    """

    def __init__(self, spec, buildable, external_type, external_location):
        """
        Construct an external package object.
        Does not check whether external type or external location are valid
        types. 
        """
        if not isinstance(spec, spack.spec.Spec):
            spec = spack.spec.Spec(spec)
        self.spec = spec
        self.external_location = external_location
        self.external_type = external_type
        self.buildable = buildable

    @property
    def version(self):
        """
        Requires that spec is well-formed and has a spec version attribute.
        Return Version object
        """
        return self.spec.version

    @property
    def name(self):
        """
        Requires that spec is well-formed and has a spec name attribute.
        Return name of the package.
        """
        return self.spec.name

    def _cmp_key(self):
        """
        Return a tuple
        Uses a tuple of attributes to compare objects of similar type
        """
        return (self.spec, self.external_location, self.external_type)

    def __str__(self):
        return str(self.spec)

    def __repr__(self):
        return "ExternalPackage({0}, {1})".format(self.spec,
                                                  self.external_location)

    @property
    def spec_section(self):
        """Return the spec section of a package entry."""
        return self.create_spec_section()

    def create_spec_section(self):
        """
        Return the specs section entry to a package configuration.
        Specs section follow the form { package_spec : path/to/package }
        """
        return syaml_dict([(str(self.spec), self.external_location)])

    def to_config_entry(self):
        """Return the config entry structure for an external package."""
        # create the inner most yaml entry
        spec_section = self.create_spec_section()
        entry = syaml_dict([("buildable", self.buildable),
                            (self.external_type, spec_section)])
        return syaml_dict([(self.name, entry)])

    @classmethod
    def create_external_package(cls, spec, external_location):
        """
        Return an external package object.

        Calls methods to detect the external type of the specified external
        package location and also to detect a version. If the version is
        not detected and a version was not specified in the spec, then it will
        output a message to notify user to input a spec with a version.

        Once it is able to determine the external type and attempts to
        determine a version, then it will call the ExternalPackage's
        constructor to create an object.
        """

        def _get_version_from_spec(package_spec):
            try:
                return str(package_spec.version)
            except spack.spec.SpecError:
                return None

        external_type = cls._find_external_type(external_location)

        if external_type == "unknown":
            tty.die("Could not detect correct path or module for %s" % spec)
        elif external_type == "paths":
            cls._validate_package_path_installation(external_location, spec)

        found_version = detect_version(external_location)
        spec_version = _get_version_from_spec(spec)

        if not found_version and not spec_version:
            tty.die("Could not detect version for package {0}\n"
                    "Please provide a spec with a version".format(spec))

        package_spec = cls._update_spec(spec, spec_version, found_version)
        buildable = False  # default setting for an external package
        external_package = cls(package_spec,
                               buildable,
                               external_type,
                               external_location)
        return external_package

    @staticmethod
    def _update_spec(spec, spec_version, found_version):
        """
        Return a spec with a version.

        Updates the spec with the version found. If there was no version
        detected then return the spec. If a version was found on the spec
        and there is a version that was detected and they do not match then
        raise an error. Otherwise, update the spec string and create a new
        Spec object from the string.
        """
        if not found_version:
            return spec
        if spec_version and spec_version != found_version:
            raise SpecVersionMisMatch(spec)
        spec_string = str(spec)
        index = len(spec.name)  # index where we want to change version
        new_spec_string = spec_string[:index] + \
                          "@{0}".format(found_version) + spec_string[index:]
        new_spec = spack.spec.Spec(new_spec_string)
        return new_spec

    @staticmethod
    def _find_external_type(external_package_location):
        """
        Return a external type detected from the given location.

        If the location is a directory or a real path then return "paths".
        Otherwise, check to see if location responds to module command.
        If it does, then return "modules".

        If neither works, return "unknown"
        """
        if os.path.isdir(external_package_location):
            return "paths"
        else:
            modulecmd = spack.util.executable.which("modulecmd")
            if modulecmd:
                modulecmd.add_default_arg("python")
                output = modulecmd("show", external_package_location,
                                   output=str, error=str)
                if "ERROR" not in output:
                    return "modules"
            return "unknown"

    @staticmethod
    def _validate_package_path_installation(path, spec):
        """
        Returns if and only if directories and/or files include the package
        name.

        Traverses a list of directories standard to an install path and checks
        whether files are found that include the package name.
        """
        def find_spec_name_match_in_directory(dirpath):
            """Search package directory for files that match package name"""
            if os.path.exists(dirpath):
                files = os.listdir(dirpath)
                for f in files:
                    if spec.name in f:
                        return True

        valid_checks = []
        for directory in ["bin", "lib", "share", "include"]:
            directory_path = llnl.util.filesystem.join_path(path, directory)
            valid_checks.append(find_spec_name_match_in_directory(
                directory_path))
        if not any(valid_checks):
            tty.die("Incorrect path: {1} for package {0}".format(path, spec))


def add_external_package(external_package, scope):
    """
    Add an external package entry to packages.yaml.
    Determines whether a package exists, if so then append to the existing
    entry. If there are no entries for the package, then add the new entry.
    """
    packages_config = PackagesConfig(scope)

    def duplicate_specs(spec, existing_specs):
        for k in existing_specs.keys():
            if spack.spec.Spec(k) == spec:
                return True
        return False

    existing_package_entry = packages_config.get_package(external_package.name)
    specs_section = existing_package_entry.specs_section()

    if existing_package_entry.is_empty():
        package_entry = external_package.to_config_entry()
        packages_config.update_package_config(package_entry)
    elif not duplicate_specs(external_package.spec, specs_section):
        existing_package_entry.update_specs(external_package.spec_section)
        new_package_entry = existing_package_entry.config_entry()
        packages_config.update_package_config(new_package_entry)
    else:
        tty.msg("Added no new external packages")


def remove_package_from_packages_config(package_spec, scope):
    """
    Remove a external package entry.

    Given a package spec, search the config file for a matching spec and
    remove it. If it is the final entry of the spec, remove the entire entry.
    """
    packages_config = PackagesConfig(scope)
    package_entry = packages_config.get_package(package_spec.name)
    previous_specs_section = package_entry.specs_section()

    if previous_specs_section:
        package_entry.remove_spec(package_spec)
    else:
        tty.die("Could not find spec {0}".format(package_spec))

    if len(previous_specs_section) == len(package_entry.specs_section()):
        raise PackageSpecInsufficientlySpecificError(package_spec)
    elif package_entry.is_spec_empty():
        packages_config.remove_entire_entry_from_config(package_spec.name)
    else:
        packages_config.update_package_config(
            package_entry.config_entry())


class PackageSpecInsufficientlySpecificError(spack.error.SpackError):
    def __init__(self, package_spec):
        super(PackageSpecInsufficientlySpecificError, self).__init__(
            "Multiple packages match package spec {0}".format(package_spec))


class SpecVersionMisMatch(spack.error.SpackError):
    def __init__(self, package_spec):
        super(SpecVersionMisMatch, self).__init__(
            "Found version and spec version do not match"
        )

class UnknownExternalType(spack.error.SpackError):
    def __init__(self, package_spec):
        super(UnknownExternalType, self).__init__(
                "Could not determine location of {}".format(package_spec))
