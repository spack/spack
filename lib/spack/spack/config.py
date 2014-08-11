##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""This module implements Spack's configuration file handling.

Configuration file scopes
===============================

When Spack runs, it pulls configuration data from several config
files, much like bash shells.  In Spack, there are two configuration
scopes:

 1. ``site``: Spack loads site-wide configuration options from
   ``$(prefix)/etc/spackconfig``.

 2. ``user``: Spack next loads per-user configuration options from
    ~/.spackconfig.

If user options have the same names as site options, the user options
take precedence.


Configuration file format
===============================

Configuration files are formatted using .gitconfig syntax, which is
much like Windows .INI format.  This format is implemented by Python's
ConfigParser class, and it's easy to read and versatile.

The file is divided into sections, like this ``compiler`` section::

     [compiler]
         cc = /usr/bin/gcc

In each section there are options (cc), and each option has a value
(/usr/bin/gcc).

Borrowing from git, we also allow named sections, e.g.:

     [compiler "gcc@4.7.3"]
         cc = /usr/bin/gcc

This is a compiler section, but it's for the specific compiler,
``gcc@4.7.3``.  ``gcc@4.7.3`` is the name.


Keys
===============================

Together, the section, name, and option, separated by periods, are
called a ``key``.  Keys can be used on the command line to set
configuration options explicitly (this is also borrowed from git).

For example, to change the C compiler used by gcc@4.7.3, you could do
this:

    spack config compiler.gcc@4.7.3.cc /usr/local/bin/gcc

That will create a named compiler section in the user's .spackconfig
like the one shown above.
"""
import os
import re
import inspect
import ConfigParser as cp

from external.ordereddict import OrderedDict
from llnl.util.lang import memoized
import spack.error

__all__ = [
    'SpackConfigParser', 'get_config', 'SpackConfigurationError',
    'InvalidConfigurationScopeError', 'InvalidSectionNameError',
    'ReadOnlySpackConfigError', 'ConfigParserError', 'NoOptionError',
    'NoSectionError']

_named_section_re = r'([^ ]+) "([^"]+)"'

"""Names of scopes and their corresponding configuration files."""
_scopes = OrderedDict({
    'site' : os.path.join(spack.etc_path, 'spackconfig'),
    'user' : os.path.expanduser('~/.spackconfig')
})

_field_regex = r'^([\w-]*)'        \
               r'(?:\.(.*(?=.)))?' \
               r'(?:\.([\w-]+))?$'

_section_regex = r'^([\w-]*)\s*' \
                 r'\"([^"]*\)\"$'


# Cache of configs -- we memoize this for performance.
_config = {}

def get_config(scope=None, **kwargs):
    """Get a Spack configuration object, which can be used to set options.

       With no arguments, this returns a SpackConfigParser with config
       options loaded from all config files.  This is how client code
       should read Spack configuration options.

       Optionally, a scope parameter can be provided.  Valid scopes
       are ``site`` and ``user``.  If a scope is provided, only the
       options from that scope's configuration file are loaded.  The
       caller can set or unset options, then call ``write()`` on the
       config object to write it back out to the original config file.

       By default, this will cache configurations and return the last
       read version of the config file.  If the config file is
       modified and you need to refresh, call get_config with the
       refresh=True keyword argument.  This will force all files to be
       re-read.
    """
    refresh = kwargs.get('refresh', False)
    if refresh:
        _config.clear()

    if scope not in _config:
        if scope is None:
            _config[scope] = SpackConfigParser([path for path in _scopes.values()])
        elif scope not in _scopes:
            raise UnknownConfigurationScopeError(scope)
        else:
            _config[scope] = SpackConfigParser(_scopes[scope])

    return _config[scope]


def get_filename(scope):
    """Get the filename for a particular config scope."""
    if not scope in _scopes:
        raise UnknownConfigurationScopeError(scope)
    return _scopes[scope]


def _parse_key(key):
    """Return the section, name, and option the field describes.
       Values are returned in a 3-tuple.

       e.g.:
       The field name ``compiler.gcc@4.7.3.cc`` refers to the 'cc' key
       in a section that looks like this:

          [compiler "gcc@4.7.3"]
              cc = /usr/local/bin/gcc

       * The section is ``compiler``
       * The name is ``gcc@4.7.3``
       * The key is ``cc``
    """
    match = re.search(_field_regex, key)
    if match:
        return match.groups()
    else:
        raise InvalidSectionNameError(key)


def _make_section_name(section, name):
    if not name:
        return section
    return '%s "%s"' % (section, name)


def _autokey(fun):
    """Allow a function to be called with a string key like
       'compiler.gcc.cc', or with the section, name, and option
       separated. Function should take at least three args, e.g.:

           fun(self, section, name, option, [...])

       This will allow the function above to be called normally or
       with a string key, e.g.:

           fun(self, key, [...])
    """
    argspec = inspect.getargspec(fun)
    fun_nargs = len(argspec[0])

    def string_key_func(*args):
        nargs = len(args)
        if nargs == fun_nargs - 2:
            section, name, option = _parse_key(args[1])
            return fun(args[0], section, name, option, *args[2:])

        elif nargs == fun_nargs:
            return fun(*args)

        else:
            raise TypeError(
                "%s takes %d or %d args (found %d)."
                % (fun.__name__, fun_nargs - 2, fun_nargs, len(args)))
    return string_key_func



class SpackConfigParser(cp.RawConfigParser):
    """Slightly modified from Python's raw config file parser to accept
       leading whitespace and preserve comments.
    """
    # Slightly modify Python option expressions to allow leading whitespace
    OPTCRE    = re.compile(r'\s*' + cp.RawConfigParser.OPTCRE.pattern)

    def __init__(self, file_or_files):
        cp.RawConfigParser.__init__(self, dict_type=OrderedDict)

        if isinstance(file_or_files, basestring):
            self.read([file_or_files])
            self.filename = file_or_files

        else:
            self.read(file_or_files)
            self.filename = None


    @_autokey
    def set_value(self, section, name, option, value):
        """Set the value for a key.  If the key is in a section or named
           section that does not yet exist, add that section.
        """
        sn = _make_section_name(section, name)
        if not self.has_section(sn):
            self.add_section(sn)

        # Allow valueless config options to be set like this:
        #     spack config set mirror https://foo.bar.com
        #
        # Instead of this, which parses incorrectly:
        #     spack config set mirror.https://foo.bar.com
        #
        if option is None:
            option = value
            value = None

        self.set(sn, option, value)


    @_autokey
    def get_value(self, section, name, option):
        """Get the value for a key.  Raises NoOptionError or NoSectionError if
           the key is not present."""
        sn = _make_section_name(section, name)

        try:
            if not option:
                # TODO: format this better
                return self.items(sn)

            return self.get(sn, option)

        # Wrap ConfigParser exceptions in SpackExceptions
        except cp.NoOptionError, e:  raise NoOptionError(e)
        except cp.NoSectionError, e: raise NoSectionError(e)
        except cp.Error, e:          raise ConfigParserError(e)


    @_autokey
    def has_value(self, section, name, option):
        """Return whether the configuration file has a value for a
           particular key."""
        sn = _make_section_name(section, name)
        return self.has_option(sn, option)


    def has_named_section(self, section, name):
        sn = _make_section_name(section, name)
        return self.has_section(sn)


    def remove_named_section(self, section, name):
        sn = _make_section_name(section, name)
        self.remove_section(sn)


    def get_section_names(self, sectype):
        """Get all named sections with the specified type.
           A named section looks like this:

               [compiler "gcc@4.7"]

           Names of sections are returned as a list, e.g.:

               ['gcc@4.7', 'intel@12.3', 'pgi@4.2']

           You can get items in the sections like this:
        """
        sections = []
        for secname in self.sections():
            match = re.match(_named_section_re, secname)
            if match:
                t, name = match.groups()
                if t == sectype:
                    sections.append(name)
        return sections


    def write(self, path_or_fp=None):
        """Write this configuration out to a file.

           If called with no arguments, this will write the
           configuration out to the file from which it was read.  If
           this config was read from multiple files, e.g. site
           configuration and then user configuration, write will
           simply raise an error.

           If called with a path or file object, this will write the
           configuration out to the supplied path or file object.
        """
        if path_or_fp is None:
            if not self.filename:
                raise ReadOnlySpackConfigError()
            path_or_fp = self.filename

        if isinstance(path_or_fp, basestring):
            path_or_fp = open(path_or_fp, 'w')

        self._write(path_or_fp)


    def _read(self, fp, fpname):
        """This is a copy of Python 2.6's _read() method, with support for
           continuation lines removed."""
        cursect = None                            # None, or a dictionary
        optname = None
        comment = 0
        lineno = 0
        e = None                                  # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            lineno = lineno + 1
            # comment or blank line?
            if ((line.strip() == '' or line[0] in '#;') or
                (line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR")):
                self._sections["comment-%d" % comment] = line
                comment += 1
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        cursect = self._sections[sectname]
                    elif sectname == cp.DEFAULTSECT:
                        cursect = self._defaults
                    else:
                        cursect = self._dict()
                        cursect['__name__'] = sectname
                        self._sections[sectname] = cursect
                    # So sections can't start with a continuation line
                    optname = None
                # no section header in the file?
                elif cursect is None:
                    raise cp.MissingSectionHeaderError(fpname, lineno, line)
                # an option line?
                else:
                    mo = self.OPTCRE.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if vi in ('=', ':') and ';' in optval:
                            # ';' is a comment delimiter only if it follows
                            # a spacing character
                            pos = optval.find(';')
                            if pos != -1 and optval[pos-1].isspace():
                                optval = optval[:pos]
                        optval = optval.strip()
                        # allow empty values
                        if optval == '""':
                            optval = ''
                        optname = self.optionxform(optname.rstrip())
                        cursect[optname] = optval
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = cp.ParsingError(fpname)
                        e.append(lineno, repr(line))
        # if any parsing errors occurred, raise an exception
        if e:
            raise e




    def _write(self, fp):
        """Write an .ini-format representation of the configuration state.

           This is taken from the default Python 2.6 source.  It writes 4
           spaces at the beginning of lines instead of no leading space.
        """
        if self._defaults:
            fp.write("[%s]\n" % cp.DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("    %s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")

        for section in self._sections:
            # Handles comments and blank lines.
            if isinstance(self._sections[section], basestring):
                fp.write(self._sections[section])
                continue

            else:
                # Allow leading whitespace
                fp.write("[%s]\n" % section)
                for (key, value) in self._sections[section].items():
                    if key != "__name__":
                        fp.write("    %s = %s\n" %
                                 (key, str(value).replace('\n', '\n\t')))


class SpackConfigurationError(spack.error.SpackError):
    def __init__(self, *args):
        super(SpackConfigurationError, self).__init__(*args)


class InvalidConfigurationScopeError(SpackConfigurationError):
    def __init__(self, scope):
        super(InvalidConfigurationScopeError, self).__init__(
            "Invalid configuration scope: '%s'" % scope,
            "Options are: %s" % ", ".join(*_scopes.values()))


class InvalidSectionNameError(SpackConfigurationError):
    """Raised when the name for a section is invalid."""
    def __init__(self, name):
        super(InvalidSectionNameError, self).__init__(
            "Invalid section specifier: '%s'" % name)


class ReadOnlySpackConfigError(SpackConfigurationError):
    """Raised when user attempts to write to a config read from multiple files."""
    def __init__(self):
        super(ReadOnlySpackConfigError, self).__init__(
            "Can only write to a single-file SpackConfigParser")


class ConfigParserError(SpackConfigurationError):
    """Wrapper for the Python ConfigParser's errors"""
    def __init__(self, error):
        super(ConfigParserError, self).__init__(str(error))
        self.error = error


class NoOptionError(ConfigParserError):
    """Wrapper for ConfigParser NoOptionError"""
    def __init__(self, error):
        super(NoOptionError, self).__init__(error)


class NoSectionError(ConfigParserError):
    """Wrapper for ConfigParser NoOptionError"""
    def __init__(self, error):
        super(NoSectionError, self).__init__(error)
