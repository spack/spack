import itertools
import os
import re

import llnl.util.filesystem
from llnl.util.lang import key_ordering
import llnl.util.tty as tty
import spack.architecture
from spack.package_prefs import VirtualInPackagesYAMLError
from spack.util.spack_yaml import syaml_dict
import spack.util.executable
import spack.spec


class PackageConfigEntry(object):
    """Class represents a package entry in a packages.yaml configuration file.

    Entries from a packages.yaml file are in the form of:
        {buildable: T or F,
         paths|modules:
             { spec1: path or module name,
               spec2: path or module name }

    Attributes:
        package_name: string name of the package
        package_entry: the dictionary entry taken from packages.yaml
        external_type: whether a package is found via paths or modules
        specs: the specs component of an entry
    """

    def __init__(self, package_name, package_entry):
        """Inits a package config entry with a package name and entry

        Finds the external type of an external package from the entry.
        And also finds the specs dictionary from the nested package entry
        """
        self.package_name = package_name
        self.package = package_entry
        self.external_type = self._find_external_type()
        self.specs = self._get_specs(self.external_type)

    def specs_section(self):
        return self.specs.copy()

    def contains_specs(self):
        return self.specs != {}

    def is_empty(self):
        return self.package == {}

    def update_specs(self, update_spec):
        """Adds specs to the specs_section of a package config.

        Updates the spec section of a package with a new spec. Requires
        that the update_spec be a key, value dict pair.

        Args:
            update_spec: spec, path or module key value pair in a dict.
        """
        self.specs.update(update_spec)
        self.package[self.external_type] = self.specs

    def remove_spec(self, spec_to_be_removed):
        """Remove a spec from the specs section

        Filter the spec section by finding a match with another Spec

        Args:
            spec_to_be_removed: a Spec object to match
        """

        filtered_specs = self._filter_specs(spec_to_be_removed)
        self.specs = filtered_specs
        self.package[self.external_type] = filtered_specs

    def _filter_specs(self, spec):
        matching_spec = spec
        if isinstance(matching_spec, str):
            matching_spec = spack.spec.Spec(matching_spec)
        filtered_specs = {}
        for pkg_spec, external in self.specs_section().iteritems():
            if spack.spec.Spec(pkg_spec) != matching_spec:
                filtered_specs[pkg_spec] = external
        return filtered_specs

    def _get_specs(self, external_type):
        return self.package.get(external_type, {})

    def _find_external_type(self):
        valid_types = ["modules", "paths"]
        for external in valid_types:
            specs_section = self._get_specs(external)
            if specs_section:
                return external

    def config_entry(self):
        """Turn a PackagesConfigEntry into a syaml dict

        Args:
            None

        Returns:
            An syaml dict to be placed in a packages config file
        """
        return {self.package_name: self.package}


class PackagesConfig(object):
    """Class represents a packages.yaml configuration file.

    PackagesConfig is an abstraction of the packages.yaml configuration file.
    With a PackagesConfig object, entries can be updated and deleted.
    The class also can return the entire contents of the configuration file.
    """

    def __init__(self, scope):
        """Inits class with a configuration scope.

        Scope is a string that can be either site/user/defaults.
        """
        self.scope = scope
        config = spack.config.get_config("packages", scope)
        virtuals = [(pkg_name, pkg_name._start_mark) for pkg_name in config
                    if spack.repo.is_virtual(pkg_name)]
        if virtuals:
            errors = ["%s: %s" % (line_info, name) for name, line_info in virtuals]
            raise VirtualInPackagesYAMLError(
                    "packages.yaml entries cannot be virtual packages:",
                    '\n'.join(errors))
        self.packages_config = config

    def get_package(self, package_name):
        """Given a package name, return a PackageConfigEntry object.

        PackageConfigEntry represents a config entry and is mutable.

        Args:
            package_name: the name of the package to retrieve.

        Returns:
            a PackageConfigEntry object.
        """
        package = self.packages_config.get(package_name, {})
        return PackageConfigEntry(package_name, package)

    def update_package_config(self, package_entry):
        """Update packages.yaml with a new entry.

        Update a package config entry. This includes appending a new spec
        or deleting an old one.

        Args:
            package_entry: a package dictionary that includes updated contents
                the entry can include either a deleted item or a new one.
        """
        spack.config.update_config("packages", package_entry, self.scope)

    def remove_entire_entry_from_config(self, package_name):
        """Remove an entire package name from the config.

        Remove the entire package entry from packages.yaml. In order for this
        to occur, the configuration file must be entirely overwritten since
        dict.update() does not update with deleted items.

        Args:
            package_name: the name of the package to be deleted.
        """
        self.packages_config.pop(package_name)
        self._overwrite_package_config()
        tty.msg("Removed {0}".format(package_name))

    def all_external_packages(self):
        """Return all the external packages listed in a packages.yaml file.

        Args:
            None
        Returns:
            a list of PackageConfigEntry's.
        """
        all_packages = []
        for package_name, entry in self.packages_config.iteritems():
            if package_name == "all":
                continue
            all_packages.append(PackageConfigEntry(package_name, entry))
        return all_packages

    def _overwrite_package_config(self):
        scope = spack.config.validate_scope(self.scope)
        scope.sections["packages"] = {'packages': self.packages_config}
        scope.write_section("packages")


def detect_version_by_prefix(path):
    """Return a version string if it is detected from a prefix.

    Return a string that matches a version format, i.e. X.X.X or a variant
    of that. Checks to see if it is a valid version and then returns that
    string.

    Args:
        path: path to the installation of a package.

    Returns:
        a string that represents the version of a package.
    """

    def directory_string_represents_version(directory_name):
        """Returns true if directory name satisfies a version format"""
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
    """Attempt to detect a version via modulecmd.

    If tclmodules are present, it uses modulecmd avail to parse the output and
    look for the version of a package.

    Args:
        module_name: The module name of a package. Requires it to be a valid
            name.

    Returns:
        the version string.
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
    """Attempts to detect the version of a package using different strategies.

    Uses different strategies to find a version either by the installed prefix
    of a package or by it's module name.

    Args:
        external_location: can either be a path string or a module name string

    Returns:
        A version string.
    """

    def execute(function_to_call_and_args):
        """Helper method to call functions with or without arguments"""
        func, args = function_to_call_and_args
        if args:
            return func(args)
        else:
            return func()

    detection_strategies = [(detect_version_by_module,
                             external_location),
                            (detect_version_by_prefix,
                             external_location)]

    successful_checks = set()
    version_attempts = map(execute, detection_strategies)
    for ver in version_attempts:
        if ver:
            successful_checks.add(ver)
    # If our checks provided us with a single version then return that.
    # Return nothing even if multiple versions were found, we only want one
    # single version and want to avoid multiple version conflicts
    if len(successful_checks) == 1:
        return successful_checks.pop()


@key_ordering
class ExternalPackage(object):
    """Class creates external package objects.

    An ExternalPackage object is constructred from a spec and the package
    location. It validates the package location and attempts to find a
    version if possible. The object can then be used to insert entries
    into packages.yaml

    Attributes:
        spec: Spec object.
        package_location:  either a path or a module name.
        external_type: either paths or modules.
        buildable: a boolean.
        version: version of the external package.
        name: name of the external package.
    """

    def __init__(self, spec, buildable, external_type, external_location):
        """Construct an external package object."""
        if not isinstance(spec, spack.spec.Spec):
            spec = spack.spec.Spec(spec)
        self.spec = spec
        self.external_location = external_location
        self.external_type = external_type
        self.buildable = buildable

    @property
    def version(self):
        return self.spec.version

    @property
    def name(self):
        return self.spec.name

    def _cmp_key(self):
        return (self.spec, self.external_location, self.external_type)

    def __str__(self):
        return str(self.spec)

    def __repr__(self):
        return "ExternalPackage({0}, {1})".format(self.spec,
                                                  self.external_location)

    def spec_section(self):
        """Getter for the spec section of a package dictionary."""
        return self.create_spec_section()

    def create_spec_section(self):
        return syaml_dict([(str(self.spec), self.external_location)])

    def to_config_entry(self):
        """Turn an external package object to an syaml dict """
        # create the inner most yaml entry
        spec_section = self.create_spec_section()
        entry = syaml_dict([("buildable", self.buildable),
                            (self.external_type, spec_section)])
        return syaml_dict([(self.name, entry)])


    @staticmethod
    def _append_version_to_string(spec_string, version, index):
        """Inserts a version into the specified index of a spec string"""
        new_spec_string = spec_string[:index] + "@{0}".format(version)  \
                          + spec_string[index:]
        return new_spec_string

    @classmethod
    def find_external_packages(cls, package_spec=None):
        """Attempts to find system packages.

        Currently, uses the modulecmd and parses for all packages. If
        a package_spec is given, the name will be used to search for packages.
        If no args are given it will attempt to find packages depending on
        the platform it is located.

        Args:
            package_spec: an optional spec object
        Returns:
            a list of ExternalPackage objects
        """
        # Packages should probably tell us how to find themselves given a 
        # System. At the moment only cray packages are supported.
        cray_prefix = "cray-"
        modulecmd = spack.util.executable.which("modulecmd")
        modulecmd.add_default_arg("python")
        cray_modules = modulecmd("avail", cray_prefix, output=str, error=str)
        matches = re.findall(r'(cray-\w+)/([\d.]+)', cray_modules)

        # Filter packages based off of valid packages in spack's database

        # Create a spec string for each package name, appends version.
        compilers = spack.compilers.all_compilers()
        arch = spack.architecture.sys_type()

        valid_packages = {}
        for package, version in matches:
            package_name = package.lstrip("cray-")
            if spack.repo.exists(package_name):
                spec_string = "{0}@{1}".format(package_name, version)
                valid_packages[spec_string] = package + "/" + version # module

        new_specs = {}
        for spec, compiler in itertools.product(valid_packages.keys(),
                                                compilers):
            module = valid_packages.get(spec)
            full_spec = spec + "%" + str(compiler) + " arch=" +arch
            spec = spack.spec.Spec(full_spec)
            new_specs[spec] = module

        external_packages = []
        for full_spec, module in new_specs.items():
            package = cls.create_external_package(full_spec, module)
            external_packages.append(package)
        return external_packages


    @classmethod
    def find_external_pacakges(cls, package_spec=None):
        """Attempts to find system packages.

        Currently, uses the modulecmd and parses for all packages. If
        a package_spec is given, the name will be used to search for packages.
        If no args are given it will attempt to find packages depending on
        the platform it is located.

        Args:
            package_spec: an optional spec object
        Returns:
            a list of ExternalPackage objects
        """
        # Packages should probably tell us how to find themselves given a 
        # System. At the moment I will only support cray packages.
        return []


    @classmethod
    def create_external_package(cls, spec, external_location):
        """Return an external package object.

        Calls methods to detect the external type of the specified external
        package location and also to detect a version. If the version is
        not detected and a version was not specified in the spec, then it will
        output a message to notify user to input a spec with a version.

        Once it is able to determine the external type and attempts to
        determine a version, then it will call the ExternalPackage's
        constructor to create an object.

        Args:
            spec: a spec string or Spec object.
            package_location: either a prefix path string or a module name.

        Returns:
            an ExternalPackage object.
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
        """Return a spec with a version.

        Updates the spec with the version found. If there was no version
        detected then return the spec. If a version was found on the spec
        and there is a version that was detected and they do not match then
        raise an error. Otherwise, update the spec string and create a new
        Spec object from the string."""
        if not found_version:
            return spec
        if spec_version and spec_version != found_version:
            raise SpecVersionMisMatch(spec)
        spec_string = str(spec)
        new_spec_string = ExternalPackage._append_version_to_string(
                spec_string, found_version, len(spec.name))
        new_spec = spack.spec.Spec(new_spec_string)
        return new_spec

    @staticmethod
    def _find_external_type(external_package_location):
        """Return a external type detected from the given location.

        If the location is a directory or a real path then return "paths".
        Otherwise, check to see if location responds to module command.
        If it does, then return "modules".

        If neither works, return "unknown" """
        if os.path.isdir(external_package_location):
            return "paths"
        else:
            modulecmd = spack.util.executable.which("modulecmd")
            if modulecmd:
                modulecmd.add_default_arg("python")
                output = modulecmd("show", external_package_location,
                                   output=str, error=str)
                print output
                if "ERROR" not in output:
                    return "modules"
            return "unknown"

    @staticmethod
    def _validate_package_path_installation(path, spec):
        """Returns if and only if directories and/or files include the package
        name.

        Traverses a list of directories standard to an install path and checks
        whether files are found that include the package name."""
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
    """Add an external package entry to packages.yaml.
    Determines whether a package exists, if so then append to the existing
    entry. If there are no entries for the package, then add the new entry."""

    def duplicate_specs(spec, existing_specs):
        for k in existing_specs.keys():
            if spack.spec.Spec(k) == spec:
                return True
        return False

    packages_config = PackagesConfig(scope)
    existing_package_entry = packages_config.get_package(external_package.name)
    specs_section = existing_package_entry.specs_section()

    if existing_package_entry.is_empty():
        package_entry = external_package.to_config_entry()
        packages_config.update_package_config(package_entry)
    elif not duplicate_specs(external_package.spec, specs_section):
        existing_package_entry.update_specs(external_package.spec_section())
        new_package_entry = existing_package_entry.config_entry()
        packages_config.update_package_config(new_package_entry)
    else:
        tty.msg("Added no new external packages")

def remove_external_package(package_spec, scope):
    """Remove the external package specified by the external package spec"""
    packages_config = ext_package.PackagesConfig(scope)
    package = packages_config.get_package(package_spec.name)
    if package.is_empty():
        tty.die("Could not find package for {0}".format(package_spec))

    matches = []
    specs = package.specs_section()
    for s in spec.keys(): # follows {spec: path/modules}
        if spack.spec.Spec(s).satisfies(package_spec):
            matches.append(s)
    if not args.all and len(matches) > 1:
        tty.error(
                "Multiple packages match spec {0}. Choose one:".format(
                    package_spec))
        collify(sorted(matches), indent=4)
        tty.msg("Or, use spack external rm -a to remove all of them.")
        sys.exit(1)

    for spec in matches:
        package.remove_spec(spec)

    if not package.contain_specs():
        packages_config.remove_entry_entry_from_config(package_spec.name)
    else:
        packages_config.update_package_config(package.config_entry())

    return matches

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
            "Could not determine location of {0}".format(package_spec))
